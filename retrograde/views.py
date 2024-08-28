from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import json
from datetime import datetime

from .models import User, Portfolio
from .test_functions.data import candle_stick_data, my_portfolios
from .test_functions.yfinance_test import chart, chart_data, portfolio_chart_data
from .test_functions.beta_test import create_regression_line_chart

def index(request):
    my_portfolios = []

    # login_as_guest_if_not_authenticated(request)

    if request.user.is_authenticated:
        my_portfolios = Portfolio.objects.filter(owner=request.user, archived=False)
    
        return render(request, "retrograde/index.html", {
            "title": "My Portfolios",
            "portfolios": my_portfolios
        })
    return HttpResponseRedirect(reverse("login", args=()))
    

def archived_portfolios(request):
    my_portfolios = []
    if request.user.is_authenticated:
        my_portfolios = Portfolio.objects.filter(owner=request.user, archived=True)
    
    return render(request, "retrograde/index.html", {
        "title": "Archived Portfolios",
        "portfolios": my_portfolios
    })

def portfolio(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    if request.user.is_authenticated and request.user == portfolio.owner:
        return render(request, "retrograde/portfolio.html", {
            "portfolio": portfolio
        })
    return HttpResponseRedirect(reverse("index", args=()))

def trade(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    if request.user.is_authenticated and request.user == portfolio.owner:
        portfolio.trade()
        return render(request, "retrograde/portfolio.html", {
            "portfolio": portfolio
        })
    return HttpResponseRedirect(reverse("index", args=()))


def asset(request, asset_ticker):
    return render(request, "retrograde/asset.html", {
        "asset": chart(asset_ticker),
        "user_timezone": request.user.timezone
    })

@login_required
def new_portfolio(request):

    if request.method == "POST":
        name = request.POST["name"]

        date_format = "%d-%m-%Y"

        # Convert the string to a datetime object
        date = datetime.strptime(request.POST["date"], date_format).date()

        initial_capital = float(request.POST["initial_capital"])
        owner = request.user

        new_portfolio = Portfolio(name=name, owner=owner, date=date, initial_capital=initial_capital)
        new_portfolio.save()

        return HttpResponseRedirect(reverse("portfolio", args=(new_portfolio.id, )))

    else:
        return render(request, "retrograde/new_portfolio.html")

@login_required
def buy_asset(request, portfolio_id):
    if request.method == "POST":
        ticker = request.POST["ticker"]
        units = request.POST["units"]

        portfolio = Portfolio.objects.get(pk=portfolio_id)
        if request.user.is_authenticated and request.user == portfolio.owner:
            portfolio.buy(ticker, float(units))
            portfolio.save()

    return HttpResponseRedirect(reverse("portfolio", args=(portfolio.id, )))

@login_required
def close_portfolio(request, portfolio_id):
    if request.user.is_authenticated and request.user == Portfolio.objects.get(pk=portfolio_id).owner:
        Portfolio.objects.get(pk=portfolio_id).delete()
    return HttpResponseRedirect(reverse("index", args=()))

@login_required
def update_portfolio(request, portfolio_id):
    if request.method == "POST":
        new_name = request.POST["new_name"]
        if request.user.is_authenticated and request.user == Portfolio.objects.get(pk=portfolio_id).owner:
            Portfolio.objects.get(pk=portfolio_id).name = new_name
        
    return HttpResponseRedirect(reverse("index", args=()))

@login_required
def archive_portfolio(request, portfolio_id):
    if request.user.is_authenticated and request.user == Portfolio.objects.get(pk=portfolio_id).owner:
        Portfolio.objects.get(pk=portfolio_id).archive()
    return HttpResponseRedirect(reverse("index", args=()))

@login_required
def unarchive_portfolio(request, portfolio_id):
    if request.user.is_authenticated and request.user == Portfolio.objects.get(pk=portfolio_id).owner:
        Portfolio.objects.get(pk=portfolio_id).unarchive()
    return HttpResponseRedirect(reverse("index", args=()))
    
@login_required
def sell_asset(request, portfolio_id):
    if request.method == "POST":
        ticker = request.POST["ticker"]
        units = request.POST["units"]

        portfolio = Portfolio.objects.get(pk=portfolio_id)
        if request.user.is_authenticated and request.user == portfolio.owner:

            portfolio.sell(ticker, float(units))
            portfolio.save()

    return HttpResponseRedirect(reverse("portfolio", args=(portfolio.id, )))

@csrf_exempt
def asset_data(request):
    print('request', request)
    data = json.loads(request.body)
    #print(data)
    asset_ticker = data['ticker']
    width = data['width']
    #print("requested chart data for", asset_ticker, width)
    return JsonResponse(chart_data(asset_ticker, width), status=200)

@csrf_exempt
def get_advice(request, portfolio_id):
    if request.method == "GET":

        portfolio = Portfolio.objects.get(pk=portfolio_id)
        if request.user.is_authenticated and request.user == portfolio.owner:
            return JsonResponse(portfolio.get_advice(), status=200)
    return HttpResponseRedirect(reverse("portfolio", args=(portfolio.id, )))

@csrf_exempt
def get_news(request, portfolio_id):
    if request.method == "GET":
        portfolio = Portfolio.objects.get(pk=portfolio_id)
        if request.user.is_authenticated and request.user == portfolio.owner:
            return JsonResponse(portfolio.get_news(), status=200)
    return HttpResponseRedirect(reverse("portfolio", args=(portfolio.id, ))) 

@csrf_exempt
def search_asset(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    if request.user.is_authenticated and request.user == Portfolio.objects.get(pk=portfolio_id).owner:
        print('request', request)
        data = json.loads(request.body)
        #print(data)
        asset_ticker = data['ticker']
        return JsonResponse(portfolio.search_asset(asset_ticker), status=200)
    return HttpResponseRedirect(reverse("index", args=()))

@csrf_exempt
def portfolio_asset_data(request, portfolio_id):
    print('request', request)
    data = json.loads(request.body)
    #print(data)
    asset_ticker = data['ticker']
    width = data['width']
    date = Portfolio.objects.get(pk=portfolio_id).date
    if request.user.is_authenticated and request.user == Portfolio.objects.get(pk=portfolio_id).owner:
    #print("requested chart data for", asset_ticker, width)
        return JsonResponse(portfolio_chart_data(asset_ticker, width, date), status=200)
    return HttpResponseRedirect(reverse("index", args=()))

@csrf_exempt
def tick_one_day(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    if request.user.is_authenticated and request.user == portfolio.owner:
        portfolio.tick("1d")
    #with open("saved_files/" + "output5.json", "w") as json_file:
    #    json.dump({"data": portfolio.data}, json_file, indent=2)
    return HttpResponseRedirect(reverse("portfolio", args=(portfolio_id, )))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "retrograde/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "retrograde/login.html")

def visitor_login(request):

    # Attempt to sign user in
    username = "Guest"
    password = ""
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "retrograde/login.html", {
            "message": "Invalid username and/or password."
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login", args=()))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "retrograde/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "retrograde/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "retrograde/register.html")


def candlestick_chart(request):
    # Sample candlestick chart data
    """ chart_data = [
        {'t': '2023-01-01', 'o': 150, 'h': 200, 'l': 100, 'c': 180},
        {'t': '2023-01-02', 'o': 180, 'h': 220, 'l': 150, 'c': 200},
        # Add more data points as needed
    ] """

    # Convert data to JSON format
    chart_data_json = json.dumps(candle_stick_data)

    # Pass the data to the template
    context = {'chart_data_json': chart_data_json}
    return render(request, 'retrograde/candlestick_chart.html', context)

def beta(request):

    # Convert data to JSON format
    scatter_plot_data = [
        {"x": 0.01, "y": 0.10},
        {"x": 0.02, "y": 0.12},
        {"x": 0.03, "y": 0.08},
        {"x": 0.04, "y": 0.15},
        {"x": 0.05, "y": 0.07},
    ]

    line_plot_data = create_regression_line_chart(scatter_plot_data)

    # Pass the data to the template
    context = {
        'scatter_plot_data': scatter_plot_data,
        'line_plot_data': line_plot_data,
    }
    return render(request, 'retrograde/beta.html', context)

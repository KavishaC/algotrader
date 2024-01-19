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
from .data import candle_stick_data, my_portfolios
from .yfinance_test import chart, chart_data, portfolio_chart_data

def index(request):
    my_portfolios = []
    if request.user.is_authenticated:
        my_portfolios = Portfolio.objects.filter(owner=request.user)
    
    return render(request, "retrograde/index.html", {
        "portfolios": my_portfolios
    })

def portfolio(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    return render(request, "retrograde/portfolio.html", {
        "portfolio": portfolio
    })

def trade(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    portfolio.trade()
    return render(request, "retrograde/portfolio.html", {
        "portfolio": portfolio
    })

def asset(request, asset_ticker):
    return render(request, "retrograde/asset.html", {
        "asset": chart(asset_ticker),
        "user_timezone": request.user.timezone
    })

@login_required
def new_portfolio(request):
    if request.method == "POST":
        name = request.POST["name"]

        date_string = "01-01-2023"
        date_format = "%m-%d-%Y"

        # Convert the string to a datetime object
        date = datetime.strptime(request.POST["date"], date_format).date()

        initial_capital = float(request.POST["initial_capital"])
        owner = request.user

        new_portfolio = Portfolio(name=name, owner=owner, date=date, initial_capital=initial_capital)
        new_portfolio.save()

        return HttpResponseRedirect(reverse("portfolio", args=(new_portfolio.id, )))

    else:
        return render(request, "retrograde/new_portfolio.html")
    
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
def portfolio_asset_data(request, portfolio_id):
    print('request', request)
    data = json.loads(request.body)
    #print(data)
    asset_ticker = data['ticker']
    width = data['width']
    date = Portfolio.objects.get(pk=portfolio_id).date
    #print("requested chart data for", asset_ticker, width)
    return JsonResponse(portfolio_chart_data(asset_ticker, width, date), status=200)

@csrf_exempt
def tick_one_day(request, portfolio_id):
    portfolio = Portfolio.objects.get(pk=portfolio_id)
    portfolio.tick("1d")
    with open("output5.json", "w") as json_file:
        json.dump({"data": portfolio.data}, json_file, indent=2)
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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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

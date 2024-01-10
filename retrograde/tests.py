from django.test import TestCase
from .models import Portfolio

# Create your tests here.

# Replace 'your_portfolio_id' with the actual ID of your portfolio
portfolio_id = 1

try:
    # Query the database to get the Portfolio instance by its ID
    portfolio = Portfolio.objects.get(pk=portfolio_id)

    # Access the 'data' field and print the 'records'
    print(portfolio.data["records"])

except Portfolio.DoesNotExist:
    print(f"Portfolio with ID {portfolio_id} does not exist.")
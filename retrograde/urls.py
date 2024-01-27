from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:portfolio_id>", views.portfolio, name="portfolio"),
    path("<int:portfolio_id>/trade", views.trade, name="trade"),
    path("asset/<str:asset_ticker>", views.asset, name="asset"),
    path('candlestick_chart/', views.candlestick_chart, name='candlestick_chart'),
    path('asset_data', views.asset_data, name='asset_data'),
    path('tick_one_minute/<int:portfolio_id>', views.tick_one_day, name='tick_one_day'),
    path("<int:portfolio_id>/asset_data", views.portfolio_asset_data, name="portfolio_asset_data"),
    path("<int:portfolio_id>/search_asset", views.search_asset, name="search_asset"),
    path("new_portfolio", views.new_portfolio, name="new_portfolio"),
    path("<int:portfolio_id>/buy", views.buy_asset, name="buy_asset"),
    path("<int:portfolio_id>/sell", views.sell_asset, name="sell_asset"),
    path("<int:portfolio_id>/close", views.close_portfolio, name="close_portfolio"),
    path("<int:portfolio_id>/update", views.update_portfolio, name="update_portfolio"),
    path("<int:portfolio_id>/archive", views.archive_portfolio, name="archive_portfolio"),
    path("<int:portfolio_id>/unarchive", views.unarchive_portfolio, name="unarchive_portfolio"),
    path("<int:portfolio_id>/get_advice", views.get_advice, name="get_advice"),
    path("<int:portfolio_id>/get_news", views.get_news, name="get_news"),
    path("archived_portfolios", views.archived_portfolios, name="archived_portfolios"),
]


from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:portfolio_id>", views.portfolio, name="portfolio"),
    path("asset/<str:asset_ticker>", views.asset, name="asset"),
    path('candlestick_chart/', views.candlestick_chart, name='candlestick_chart'),
    path('asset_data', views.asset_data, name='asset_data'),
    path('tick_one_minute/<int:portfolio_id>', views.tick_one_minute, name='tick_one_minute'),
    path('tick_one_minute/<int:portfolio_id>', views.tick_one_day, name='tick_one_day')

]


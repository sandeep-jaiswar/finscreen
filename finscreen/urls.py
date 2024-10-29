from django.urls import path
from . import views

urlpatterns = [
    path('scrap/', views.scrap_data),
    path('history/<str:symbol>/', views.get_stock_history),
    path('info/<str:symbol>/', views.get_stock_info),
    path('actions/<str:symbol>/', views.get_stock_actions),
    path('dividends/<str:symbol>/', views.get_stock_dividends),
    path('splits/<str:symbol>/', views.get_stock_splits),
    path('financials/<str:symbol>/', views.get_stock_financials),
    path('quarterly_financials/<str:symbol>/', views.get_stock_quarterly_financials),
    path('sustainability/<str:symbol>/', views.get_stock_sustainability),
    path('recommendations/<str:symbol>/', views.get_stock_recommendations),
    path('earnings/<str:symbol>/', views.get_stock_earnings),
    path('quarterly_earnings/<str:symbol>/', views.get_stock_quarterly_earnings),
    path('major_holders/<str:symbol>/', views.get_stock_major_holders),
    path('institutional_holders/<str:symbol>/', views.get_stock_institutional_holders),
    path('calendar/<str:symbol>/', views.get_stock_calendar),
    path('options/<str:symbol>/', views.get_stock_options),
    path('option_chain/<str:symbol>/<str:expiration>/', views.get_stock_option_chain),
    path('isin/<str:symbol>/', views.get_stock_isin),
    path('news/<str:symbol>/', views.get_stock_news)
]

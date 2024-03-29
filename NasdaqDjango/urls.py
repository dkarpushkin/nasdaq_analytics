"""NasdaqDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from historical_data.views import (
    HistoricalRecordsTemplateView, HistoricalRecordsJsonView, PriceAnalyticsJsonView, PriceAnalyticsTemplateView,
    PriceDeltaJsonView, PriceDeltaTemplateView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('<str:ticker>/', HistoricalRecordsTemplateView.as_view()),
    path('api/<str:ticker>/', HistoricalRecordsJsonView.as_view()),

    path('<str:ticker>/analytics', PriceAnalyticsTemplateView.as_view()),
    path('api/<str:ticker>/analytics', PriceAnalyticsJsonView.as_view()),

    path('<str:ticker>/delta', PriceDeltaTemplateView.as_view()),
    path('api/<str:ticker>/delta', PriceDeltaJsonView.as_view()),
]

from django.urls import path

from . import views

app_name = 'sensor'
urlpatterns = [
    # URL for TemperatureHumidityAPI (get/post/delete)
    path('sensor/temperaturehumidity', views.TemperatureHumidityAPI.as_view()),

    # URL for DailyTemperatureHumidityAPI (get)
    path('sensor/dailydata', views.DailyTemperatureHumidityAPI.as_view()),

    # URL for WeeklyTemperatureHumidityAPI (get)
    path('sensor/weeklydata', views.WeeklyTemperatureHumidityAPI.as_view()),

    # URL for MonthlyTemperatureHumidityAPI (get)
    path('sensor/monthlydata', views.MonthlyTemperatureHumidityAPI.as_view()),

    # URL for IRQAPI (get/post/delete)
    path('sensor/iaq', views.IAQAPI.as_view()),

    # URL for DailyTemperatureHumidityAPI (get)
    path('sensor/dailyiaqdata', views.DailyIAQAPI.as_view()),

    # URL for WeeklyTemperatureHumidityAPI (get)
    path('sensor/weeklyiaqdata', views.WeeklyIAQAPI.as_view()),

    # URL for MonthlyTemperatureHumidityAPI (get)
    path('sensor/monthlyiaqdata', views.MonthlyIAQAPI.as_view()),
]

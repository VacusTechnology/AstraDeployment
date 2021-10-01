from django.urls import path

from . import views

app_name = 'employee'
urlpatterns = [
    # URL for EmployeeTagAPI (get/post/delete)
    path('employee/tags', views.EmployeeTagAPI.as_view()),
    
    # URL for EmployeeRegistrationAPI (get/post/delete/patch)
    path('employee/registration', views.EmployeeRegistrationAPI.as_view()),
    
    # URL for EmployeeRegistrationAPI for tracking(get)
    path('employee/tracking', views.EmployeeTrackingAPI.as_view()),
    
    # URL for DistanceCalculationAPI for tracking(get)
    path('employee/distance', views.DistanceCalculationAPI.as_view()),
]

from django.db import models

from common.models import FloorMap


""" EmployeeTag model: """
class EmployeeTag(models.Model):
    tagid = models.CharField(unique=True, max_length=20)
    battery = models.FloatField()
    lastseen = models.DateTimeField(auto_now=True) 
    x = models.FloatField()
    y = models.FloatField()
    floor = models.ForeignKey(FloorMap, on_delete=models.SET_NULL, null=True)


""" EmployeeRegistration model: """
class EmployeeRegistration(models.Model):
    tagid = models.ForeignKey(EmployeeTag, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    empid = models.CharField(max_length=100)
    email = models.CharField(max_length=254)
    phoneno = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    intime = models.DateTimeField()
    

""" EmployeeAttendance model: """

""" DistanceTracking model: """
class DistanceTracking(models.Model):
    tag1 = models.ForeignKey(EmployeeRegistration, on_delete=models.CASCADE, related_name="tag1")
    tag2 = models.ForeignKey(EmployeeRegistration, on_delete=models.CASCADE, related_name="tag2")
    distance = models.IntegerField()
    timestamp = models.DateTimeField()
    
""" DistanceCalculation model """
class DistanceCalculation(models.Model):
    empid = models.CharField(max_length=100)
    name1 = models.CharField(max_length=100)
    name2 = models.CharField(max_length=100)
    starttime =  models.DateTimeField()
    endtime =  models.DateTimeField()
    duration = models.CharField(max_length=50)

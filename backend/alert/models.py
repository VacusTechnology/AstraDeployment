from django.db import models

# Create your models here.
from employee.models import EmployeeTag


class Alert(models.Model):
    value = models.IntegerField()
    timestamp = models.DateTimeField()
    asset = models.ForeignKey(EmployeeTag, on_delete=models.CASCADE)

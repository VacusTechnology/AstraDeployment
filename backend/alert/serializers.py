from rest_framework import serializers

from .models import Alert
from employee.serializers import EmployeeTagSerializer


class AlertSerializer(serializers.ModelSerializer):
    asset = EmployeeTagSerializer()

    class Meta:
        model = Alert
        fields = ['value', 'timestamp', 'asset']

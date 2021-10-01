from rest_framework import serializers

from .models import EmployeeTag, EmployeeRegistration, DistanceCalculation


""" Serializer for EmployeeTag Model """
class EmployeeTagSerializer(serializers.ModelSerializer):    
    class Meta:
        model = EmployeeTag
        fields = "__all__"
        
    
""" Serializer for EmployeeRegistration Model """
class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    tagid = EmployeeTagSerializer()
    
    class Meta:
        model = EmployeeRegistration
        fields = "__all__"    
        

""" Serializer for DistanceCalculation Model """
class DistanceCalculationSerializer(serializers.ModelSerializer):    
    class Meta:
        model = DistanceCalculation
        fields = "__all__"  

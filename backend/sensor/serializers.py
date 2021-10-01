from rest_framework import serializers

from .models import TemperatureHumidity, IAQ, DailyTemperatureHumidity, DailyIAQ


""" Serializer for TemperatureHumidity Model """


class TemperatureHumiditySerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureHumidity
        fields = "__all__"


""" Serializer for IRQ Model """


class IAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = IAQ
        fields = "__all__"


""" Serializer for Daily, Weekly and Monthly TemperatureHumidity Model """


class SensorSerializer(serializers.ModelSerializer):
    asset = TemperatureHumiditySerializer()

    class Meta:
        model = DailyTemperatureHumidity
        fields = "__all__"


""" Serializer for Daily, Weekly and Monthly IAQ Model """


class IAQSensorSerializer(serializers.ModelSerializer):
    asset = IAQSerializer()

    class Meta:
        model = DailyIAQ
        fields = "__all__"

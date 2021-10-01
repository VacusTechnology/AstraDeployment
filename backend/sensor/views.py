from django.shortcuts import render

from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from calendar import monthrange

from common.models import FloorMap
from .models import TemperatureHumidity, IAQ, DailyTemperatureHumidity, WeeklyTemperatureHumidity, MonthlyTemperatureHumidity, DailyIAQ, WeeklyIAQ, MonthlyIAQ
from .serializers import TemperatureHumiditySerializer, IAQSerializer, SensorSerializer, IAQSensorSerializer


""" API for TemperatureHumidity """


class TemperatureHumidityAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ POST method to store details of master gateway with floor it is attached """
    @staticmethod
    def post(request):
        try:
            var = TemperatureHumidity()
            var.macid = request.data.get("macaddress")
            var.temperature = 0.0
            var.humidity = 0.0
            var.floor = FloorMap.objects.get(id=request.data.get("id"))
            var.x1 = request.data.get("x1")
            var.y1 = request.data.get("y1")
            var.x2 = request.data.get("x2")
            var.y2 = request.data.get("y2")
            var.battery = 0.0
            var.save()
            return Response(status=status.HTTP_201_CREATED)

        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    """ GET method to retrieve all details """
    @staticmethod
    def get(request):
        try:
            if request.GET.get("floorid"):
                data = TemperatureHumidity.objects.filter(
                    floor=request.GET.get("floorid"))
            else:
                data = TemperatureHumidity.objects.all()
            if data:
                ser = TemperatureHumiditySerializer(data, many=True)
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    """ DELETE method to delete particular master along with all slaves registered under master """
    @staticmethod
    def delete(request):
        try:
            data = TemperatureHumidity.objects.filter(
                macid=request.data.get("macaddress"))
            if data:
                data.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DailyTemperatureHumidityAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            currentDate = datetime.date.today().strftime("%Y-%m-%d")

            asset = TemperatureHumidity.objects.get(
                macid=request.GET.get("macaddress"))
            sensor = DailyTemperatureHumidity.objects.filter(
                asset=asset, timestamp__startswith=currentDate)
            if sensor.exists():
                thSerializer = SensorSerializer(sensor, many=True)
                return Response(thSerializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class WeeklyTemperatureHumidityAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            currentDate = datetime.date.today()
            lastweekdate = currentDate - datetime.timedelta(days=7)
            tmwdate = currentDate + datetime.timedelta(days=1)

            asset = TemperatureHumidity.objects.get(
                macid=request.GET.get("macaddress"))
            sensor = WeeklyTemperatureHumidity.objects.filter(
                asset=asset, timestamp__gte=lastweekdate, timestamp__lte=tmwdate)
            if sensor.exists():
                thSerializer = SensorSerializer(sensor, many=True)
                return Response(thSerializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MonthlyTemperatureHumidityAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            currentDate = datetime.date.today()
            month = currentDate.month
            year = currentDate.year
            if month < 10:
                month = "0"+str(month)
            dt = str(year)+"-"+str(month)

            asset = TemperatureHumidity.objects.get(
                macid=request.GET.get("macaddress"))
            sensor = MonthlyTemperatureHumidity.objects.filter(
                asset=asset, timestamp__startswith=dt)
            if sensor.exists():
                thSerializer = SensorSerializer(sensor, many=True)
                return Response(thSerializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)


""" API for IAQ """


class IAQAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ POST method to store details of slave gateway with master it is attached """
    @staticmethod
    def post(request):
        try:
            iaq = IAQ()
            iaq.macid = request.data.get("macaddress")
            iaq.battery = 0.0
            iaq.co2 = 0.0
            iaq.tvoc = 0.0
            iaq.floor = FloorMap.objects.get(id=request.data.get("id"))
            iaq.x = request.data.get("x")
            iaq.y = request.data.get("y")
            iaq.save()
            return Response(status=status.HTTP_201_CREATED)

        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    """ GET method to retrieve all details """
    @staticmethod
    def get(request):
        try:
            if request.GET.get("floorid"):
                data = IAQ.objects.filter(floor=request.GET.get("floorid"))
            else:
                data = IAQ.objects.all()
            if data:
                ser = IAQSerializer(data, many=True)
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    """ DELETE method to delete particular slave details"""
    @staticmethod
    def delete(request):
        try:
            data = IAQ.objects.filter(macid=request.data.get("macaddress"))
            if data:
                data.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DailyIAQAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            currentDate = datetime.date.today().strftime("%Y-%m-%d")

            asset = IAQ.objects.get(
                macid=request.GET.get("macaddress"))
            print(asset.id)
            sensor = DailyIAQ.objects.filter(
                asset=asset, timestamp__startswith=currentDate)
            if sensor.exists():
                thSerializer = IAQSensorSerializer(sensor, many=True)
                return Response(thSerializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class WeeklyIAQAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            currentDate = datetime.date.today()
            lastweekdate = currentDate - datetime.timedelta(days=7)
            tmwdate = currentDate + datetime.timedelta(days=1)

            asset = IAQ.objects.get(
                macid=request.GET.get("macaddress"))
            sensor = WeeklyIAQ.objects.filter(
                asset=asset, timestamp__gte=lastweekdate, timestamp__lte=tmwdate)
            if sensor.exists():
                thSerializer = IAQSensorSerializer(sensor, many=True)
                return Response(thSerializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MonthlyIAQAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            currentDate = datetime.date.today()
            month = currentDate.month
            year = currentDate.year
            if month < 10:
                month = "0"+str(month)
            dt = str(year)+"-"+str(month)

            asset = IAQ.objects.get(
                macid=request.GET.get("macaddress"))
            sensor = MonthlyIAQ.objects.filter(
                asset=asset, timestamp__startswith=dt)
            if sensor.exists():
                thSerializer = IAQSensorSerializer(sensor, many=True)
                return Response(thSerializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)

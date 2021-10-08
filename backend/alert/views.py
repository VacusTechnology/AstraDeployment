from django.shortcuts import render
import datetime
from django.shortcuts import render

from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Alert
from .serializers import AlertSerializer


class Alerts(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            currentDate = datetime.date.today().strftime("%Y-%m-%d")
            alerts = Alert.objects.filter(timestamp__startswith=currentDate, value__gt=0)
            alertSerializer = AlertSerializer(alerts, many=True)
            return Response(alertSerializer.data, status=status.HTTP_200_OK)

        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)

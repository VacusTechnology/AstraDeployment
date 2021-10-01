from django.shortcuts import render

from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SignalRepeator
from .serializers import SignalRepeatorSerializer


""" API for SignalRepeator """
class SignalRepeatorAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ POST method to store details of slave gateway with master it is attached """
    @staticmethod
    def post(request):
        try:
            slave = SignalRepeator()
            slave.macid = request.data.get("macaddress")
            slave.save()
            return Response(status=status.HTTP_200_OK)

        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    """ GET method to retrieve all details """
    @staticmethod
    def get(request):
        try:
            data = SignalRepeator.objects.all()
            ser = SignalRepeatorSerializer(data, many=True)
            return Response(ser.data, status=status.HTTP_200_OK)

        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
    """ DELETE method to delete particular slave details"""
    @staticmethod
    def delete(request):
        try:
            data = SignalRepeator.objects.filter(macid=request.data.get("macaddress"))
            if data:
                data.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST)


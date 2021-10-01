from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import FloorMap
from .serializers import FloorMapSerializer

""" API for login to application
    after successfull login maintains session data in browser storage"""
class loginAPI(APIView):

    @staticmethod
    def post(request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)


""" API for logout from application
    after logout remove session data from browser storage"""
class logoutAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            logout(request)
            return Response(status=status.HTTP_200_OK)
            
        except Exception as err:
            return Response(status=HTTP_400_BAD_REQUEST)


""" API for FloorMap model """
class FloorMapAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ GET method to retrieve all floor map details """
    def get(self, request):
        maps = FloorMap.objects.all()
        serializer = FloorMapSerializer(maps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """ POST method to store floor map image with its name, height and width """
    def post(self, request):
        try:
            mapSerializer = FloorMapSerializer(data=request.data)
            if mapSerializer.is_valid():
                mapSerializer.save()
                return Response(mapSerializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(mapSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as err:
           print(err)
           return Response(status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render

from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime

from .models import EmployeeTag, EmployeeRegistration, DistanceCalculation
from .serializers import EmployeeTagSerializer, EmployeeRegistrationSerializer, DistanceCalculationSerializer


""" API for MasterGateway """


class EmployeeTagAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ POST method to store new tag """
    @staticmethod
    def post(request):
        try:
            var = EmployeeTag()
            var.tagid = request.data.get("macaddress")
            var.battery = 0.0
            var.x = 0.0
            var.y = 0.0
            var.floor = None
            var.save()
            return Response(status=status.HTTP_201_CREATED)

        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    """ GET method to retrieve all details """
    @staticmethod
    def get(request):
        try:
            data = EmployeeTag.objects.raw(
                "select * from employee_employeetag where id in (select tagid_id from employee_employeeregistration)")
            ser = EmployeeTagSerializer(data, many=True)
            return Response(ser.data, status=status.HTTP_200_OK)

        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    """ DELETE method to delete particular master along with all slaves registered under master """
    @staticmethod
    def delete(request):
        try:
            data = EmployeeTag.objects.filter(
                tagid=request.data.get("macaddress"))
            if data:
                data.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


""" API for EmployeeRegistration """


class EmployeeRegistrationAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ POST method to add employee"""
    @staticmethod
    def post(request):
        try:
            emp = EmployeeRegistration()
            emp.tagid = None
            emp.name = request.data.get("empname")
            emp.empid = request.data.get("empid")
            emp.email = request.data.get("mailid")
            emp.phoneno = request.data.get("phoneno")
            emp.address = request.data.get("address")
            emp.intime = "1947-08-15 00:00:00"
            emp.save()
            return Response(status=status.HTTP_201_CREATED)

        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    """ GET method to retrieve all details of employee"""
    @staticmethod
    def get(request):
        try:
            if request.GET.get("key") == "all":
                data = EmployeeRegistration.objects.all()
                ser = EmployeeRegistrationSerializer(data, many=True)
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                emp = EmployeeRegistration.objects.filter(
                    empid=request.GET.get("key")).first()
                if emp:
                    ser = EmployeeRegistrationSerializer(emp)
                    return Response(ser.data, status=status.HTTP_200_OK)
                else:
                    return Response(ser.data, status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    """ DELETE method to delete particular employee details """
    @staticmethod
    def delete(request):
        try:
            data = EmployeeRegistration.objects.filter(
                empid=request.data.get("empid"))
            if data:
                data.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

    """ UPDATE method to allocate tag to employee """
    @staticmethod
    def patch(request):
        try:
            tag = EmployeeTag.objects.get(tagid=request.data.get("tagid"))
            emp = EmployeeRegistration.objects.get(
                empid=request.data.get("empid"))
            emp.tagid = tag
            currdate = datetime.datetime.today().date()
            print(str(emp.intime)[0:10], str(currdate))
            if str(emp.intime)[0:10] != str(currdate):
                emp.intime = datetime.datetime.now()
            emp.save()
            return Response(status=status.HTTP_200_OK)

        except Exception as err:
            print(err)
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


""" API for EmployeeRegistration """


class EmployeeTrackingAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ GET method to add employee"""
    @staticmethod
    def get(request):
        try:
            #emp = EmployeeRegistration.objects.raw("select * from employee_employeeregistration where tagid_id in (select id from employee_employeetag where floor_id="+request.GET.get("floorid")+")")
            emp = EmployeeRegistration.objects.filter(
                tagid__floor=request.GET.get("floorid"))
            if emp:
                ser = EmployeeRegistrationSerializer(emp, many=True)
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)


""" API for Employee Distance Tracking """


class DistanceCalculationAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    """ GET method to add employee"""
    @staticmethod
    def get(request):
        try:
            print(request.GET.get("empid"))
            emp = EmployeeRegistration.objects.get(
                empid=request.GET.get("empid"))
            data = DistanceCalculation.objects.filter(empid=emp.id)
            print(data)
            if data:
                ser = DistanceCalculationSerializer(data, many=True)
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print(err)
            return Response(status=status.HTTP_400_BAD_REQUEST)

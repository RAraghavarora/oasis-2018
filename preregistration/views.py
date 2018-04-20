# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from preregistration.serializers import *
# Create your views here.



@api_view(['POST'])
def index(request):

    if request.method=='POST':
        email=request.data['email_address'].replace('%40','@')
        if Roctaves.objects.filter(email_address=email):
            return Response({'message':'email exists'})
        mobile_number=str(request.data['phone'])
        if len (mobile_number)==10:
            try:
                number=int(mobile_number)
                roctaves=Roctaves()
                roctaves.name=request.data['name']
                roctaves.city=request.data['city']
                if request.data['gender']=='M':
                    roctaves.gender='Male'
                elif request.data['gender']=='F':
                    roctaves.gender='Female'
                roctaves.phone='91'+mobile_number
                roctaves.email_address=email
                serializer=RoctaveSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors,status=400)
            except ValueError:
                return Response({'message':'Invalid'})
        else:
            return Response({'message':'Invalid'})



    

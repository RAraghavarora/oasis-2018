# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import *
from django.http import HttpResponse,JsonResponse
from preregistration.serializers import *
import sys
import re
# Create your views here.


@api_view(['POST'])
def index(request):

    if request.method=='POST':
        # print request.data
        email=request.data['email_address'].replace('%40','@')
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
            return Response({"message":"Invalid email"})
        #if Roctaves.objects.filter(email_address=email):
         #   return Response({'message':'email exists'})
        mobile_number=str(request.data['phone'])
        if len (mobile_number)==10:
            try:
                number=int(mobile_number)
                roctaves=Roctaves()
                roctaves.name=request.data['name']
                roctaves.elimination_preference=request.data['elimination_preference']
                roctaves.genre=request.data['genre']
                roctaves.number_of_participants=abs(int(request.data['number_of_participants']))
                roctaves.entry1=request.data['entry1']
                roctaves.entry2=request.data['entry2']
                try:
                    roctaves.enteries=request.data['enteries']
                except:
                    pass
                roctaves.phone='91'+mobile_number
                try:
                    roctaves.email_address=email
                except:
                    return Response({"message":"Invalid email address"})
                roctaves.save()
                return Response({'message':'Your registration is complete'})
            except ValueError:
                return Response({'message':'Data entered is not in proper format'})
        else:
            return Response({'message':'Mobile number is incorrect'})



    
#blsb

#w

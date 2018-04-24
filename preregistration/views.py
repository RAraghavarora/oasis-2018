# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import *
from .serializers import *
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


@api_view(['POST'])
def gen_index(request):

    if request.method=='POST':
        print(request.data)
        email=request.data['email_address'].replace('%40','@')
        # if Participant.objects.filter(email_address=email):
        #     return Response({'message':'Email already exists! Please try another email'})
        mobile_number=str(request.data['phone'])
        if len (mobile_number)==10:
            try:
                number=int(mobile_number)
                participant = GenParticipant()
                participant.name=request.data['name']
                participant.city=request.data['city']
                participant.gender='Male'
                participant.phone='91'+mobile_number
                participant.email_address=email
                serializer=GenParticipantSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors,status=400)
            except ValueError:
                return Response({'message':'Please input valid credentials.'})
        else:
            return Response({'message':'Please input valid credentials.'})

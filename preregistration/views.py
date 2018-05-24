# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import sys

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import unicodedata
from .models import *
from .serializers import *
from preregistration.serializers import *

RapWarParticipationCities = {'Delhi': 'Delhi', 'Mumbai': 'Mumbai', 'Kolkata': 'Kolkata'}
PoetrySlamCities = {'Delhi': 'Delhi', 'Mumbai': 'Mumbai', 'Jaipur': 'Jaipur', 'Lucknow':'Lucknow'}
@api_view(['POST'])
def index(request):

    """ Create new Roctaves Teams """

    if request.method=='POST':
        try:
            email=request.data['email_address'].replace('%40','@')

            if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
                return Response({"message":"Invalid email"})

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

        except KeyError as missing_data:
                return Response({'message':'Data is Missing: {}'.format(missing_data)})


@api_view(['POST'])
def gen_index(request):

    """ create new GenParticipant """

    try:
        if request.method=='POST':
            print(request.data)

            email=request.data['email_address'].replace('%40','@')
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

    except KeyError as missing_data:
            return Response({'message':'Data is Missing: {}'.format(missing_data)})

@api_view(['POST'])
def PoetrySlamRegistration(request):
#ps here is for poetryslam

    if request.method=='POST':
        try:
            email=request.data['email_address'].replace('%40','@')

            if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
                return Response({"message":"Invalid email"})

            mobile_number=str(request.data['phone'])

            if len (mobile_number)==10:
                try:
                    number=int(mobile_number)
                    poetryslam=PoetrySlam()
                    poetryslam.name=request.data['name']
                    poetryslam.city=request.data['city']
                    poetryslam.phone='91'+mobile_number
                    try:
                        poetryslam.email_address=email
                    except:
                        return Response({"message":"Invalid email address"})
                    poetryslam.save()
                    return Response({'message':'Your registration is complete'})
                except ValueError:
                    return Response({'message':'Data entered is not in proper format'})
            else:
                return Response({'message':'Mobile number is incorrect'})

        except KeyError as missing_data:
                return Response({'message':'Data is Missing: {}'.format(missing_data)})


@api_view(['POST'])
def RapWarsRegistration(request):
#rw is for rapwars

    if request.method=='POST':
        try:
            email=request.data['email_address'].replace('%40','@')

            if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
                return Response({"message":"Invalid email"})

            mobile_number=str(request.data['phone'])

            if len (mobile_number)==10:
                try:
                    number=int(mobile_number)
                    rapwars = RapWars()
                    rapwars.name=request.data['name']
                    try:
                        rapwars.rapper_name=request.data['rapper_name']
                    except:
                        pass
                    rapwars.city = request.data['city']
                    rapwars.phone='91'+mobile_number
                    city_participation = request.data['city_of_participation']
                    flag = 0
                    for key in RapWarParticipationCities.keys():
                        if (city_participation.casefold() == key.casefold()):
                            flag = 1
                    if (flag==0):
                        return Response({'message': 'Invalid City of Participation'})
                    rapwars.city_of_participation = request.data['city_of_participation']
                    try:
                        rapwars.email_address=email
                    except:
                        return Response({"message":"Invalid email address"})
                    rapwars.save()
                    return Response({'message':'Your registration is complete'})
                except ValueError:
                    return Response({'message':'Data entered is not in proper format'})
            else:
                return Response({'message':'Mobile number is incorrect'})

        except KeyError as missing_data:
                return Response({'message':'Data is Missing: {}'.format(missing_data)})

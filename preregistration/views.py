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
        if Participant.objects.filter(email_address=email):
            return Response({'message':'Email already exists! Please try another email'})
        mobile_number=str(request.data['phone'])
        if len (mobile_number)==10:
            try:
                number=int(mobile_number)
                participant = Participant()
                participant.name=request.data['name']
                participant.city=request.data['city']
                if request.data['gender']=='M':
                    participant.gender='Male'
                elif request.data['gender']=='F':
                    participant.gender='Female'
                participant.phone='91'+mobile_number
                participant.email_address=email
                serializer=ParticipantSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors,status=400)
            except ValueError:
                return Response({'message':'Please input valid credentials.'})
        else:
            return Response({'message':'Please input valid credentials.'})

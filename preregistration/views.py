# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import sys

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from events.models import *
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import unicodedata
from .models import *
from .serializers import *
from preregistration.serializers import *

RapWarsParticipationCities = {'Delhi': 'Delhi', 'Mumbai': 'Mumbai', 'Kolkata': 'Kolkata'}
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
			try:
				email=request.data['email_address'].replace('%40','@')
				if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
					return Response({"message":"Invalid email"})
			except KeyError:
				email=""

			mobile_number=str(request.data['phone'])

			if len (mobile_number)==10:
				try:
					number=int(mobile_number)
					poetryslam=PoetrySlamExtension()
					gp = GenParticipant()
					gp.name=request.data['name']
					flag = 0
					city_1 = request.data['city']
					for sity in PoetrySlamCities.keys():
						if(city_1.lower() == sity.lower()):
							flag = 1
					if(flag == 0):
						return Response({'message':'Invalid city. Please enter correct city'})
					gp.city = request.data['city']
					gp.phone='91'+mobile_number
					try:
						gp.email_address=email
					except:
						return Response({"message":"Invalid email address"})
					gp.save()
					poetryslam.participant = gp
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
			try:
				email=request.data['email_address'].replace('%40','@')
				if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
					return Response({"message":"Invalid email"})
			except KeyError:
				email=""

			mobile_number=str(request.data['phone'])

			if len (mobile_number)==10:
				try:
					number=int(mobile_number)
					rapwars = RapWarsExtension()
					gp = GenParticipant()
					gp.name=request.data['name']
					try:
						rapwars.rapper_name=request.data['rapper_name']
					except:
						pass

					gp.city = request.data['city']
					gp.phone='91'+mobile_number
					city_of_participation = request.data['city_of_participation']
					flag = 0
					for sity in RapWarsParticipationCities.keys():
						if(city_of_participation.lower() == sity.lower()):
							flag = 1
					if(flag == 0):
						return Response({'message':'Invalid city. Please enter correct city'})

					rapwars.city_of_participation = request.data['city_of_participation']
					try:
						gp.email_address=email
					except:
						return Response({"message":"Invalid email address"})
					gp.save()
					rapwars.participant = gp
					rapwars.save()
					return Response({'message':'Your registration is complete'})
				except ValueError:
					return Response({'message':'Data entered is not in proper format'})
			else:
				return Response({'message':'Mobile number is incorrect'})

		except KeyError as missing_data:
				return Response({'message':'Data is Missing: {}'.format(missing_data)})

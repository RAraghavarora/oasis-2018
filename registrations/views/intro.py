# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import json
import urllib
import unicodedata

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from events.models import *
from registrations.models import *
from registrations.serializers import *


class PreRegistration(APIView):

	def get(self, request, format=None):
		college_list = College.objects.all()
		serializer = CollegeSerializer(college_list, many = True)
		return Response(serializer.data)

	def post(self, request, format=None):
		try:
			''' Begin reCAPTCHA validation '''
			recaptcha_response = request.data['g-recaptcha-response']
			url = 'https://www.google.com/recaptcha/api/siteverify'
			values = {
			    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
			    'response': recaptcha_response
			}
			data = urllib.parse.urlencode(values).encode()
			req =  urllib.request.Request(url, data=data)
			response = urllib.request.urlopen(req)
			result = json.loads(response.read().decode())
			''' End reCAPTCHA validation '''

			if not result['success']:
				response = Response({'message' : 'Invalid reCaptcha', 'x_status': 0})
				response.delete_cookie('sessionid')
				return response

			try:
				college = College.objects.get(name = request.data['college'])
			except:
				response = Response({'message' : 'Nice try.... stay away from dev tools kid.', 'x_status': 999})
				response.delete_cookie('sessionid')
				return response

			email_id = request.data['email_id'].lower().strip()
			if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_id):
				response = Response({'message' : 'Nice try.... stay away from dev tools kid.', 'x_status': 999})
				response.delete_cookie('sessionid')
				return response
			try:
				if IntroReg.objects.get(email_id = email_id):
					response = Response({'message' : 'Email already registered.', 'x_status': 2})
					response.delete_cookie('session_id')
					return response
			except:
				pass

			mobile_no = str(request.data['mobile_no'])
			if(len(mobile_no) is not int(10)):
				response =  Response({'message' : 'Incorrect Mobile Number.', 'x_status': 3})
				response.delete_cookie('session_id')
				return response

			name = request.data['name'].lower()


			participant = IntroReg()

			participant.college = college
			participant.email_id = email_id
			participant.name = name
			participant.mobile_no = int(mobile_no)

			participant.save()

			data = {'email_id': email_id, 'name' : name, 'mobile_no' : mobile_no}
			return Response({"message":"Your registration is complete."})

		except KeyError as missing_data:
			response = Response({'message':'Data is Missing: {}'.format(missing_data), 'x_status': 4})
			response.delete_cookie('sessionid')
			return response

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import unicodedata

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from events.models import *
from registrations.models import *
from registrations.serializers import *


@api_view(['GET', 'POST'])
def PreRegistration(request):

	if request.method == 'GET':
		college_list = College.objects.all()
		serializer = CollegeSerializer(college_list, many = True)
		return Response(serializer.data)

	if request.method == 'POST':
		try:
			college_name = request.data['college']

			if college_name.upper() == 'OTHERS':
				college_name = request.data['other_college'].upper()
				try:
					if College.objects.get(name = college_name):
						pass
				except:
					college = College()
					college.name = request.data['other_college'].upper()
					college.save()

			college = College.objects.get(name = college_name)

			email_id = request.data['email_id'].lower().strip()
			if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_id):
				response = Response({"message":"Invalid email"})
				response.delete_cookie('sessionid')
				return response
			try:
				if IntroReg.objects.get(email_id = email_id):
					response = Response({'message' : 'Email already registered.'})
					response.delete_cookie('session_id')
					return response
			except:
				pass

			mobile_no = str(request.data['mobile_no'])
			print len(mobile_no)
			if(len(mobile_no) is not int(10)):
				response =  Response({'message' : 'Incorrect Mobile Number.'})
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
			response = Response({'message':'Data is Missing: {}'.format(missing_data)})
			response.delete_cookie('sessionid')
			return response

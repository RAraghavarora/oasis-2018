# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *
from events.models import *
from registrations.serializers import *

import unicodedata

@api_view(['GET', 'POST'])
def PreRegistration(request):

	if request.method == 'GET':
		college_list = College.objects.all()
		serializer = CollegeSerializer(college_list, many = True)
		print serializer.data
		return Response(serializer.data)

	if request.method == 'POST':

		college_name = request.data['college']

		if college_name == 'Others':
			college = College()
			college.name = request.data['other_college']
			college.save()
		
		college = College.objects.get(name = college_name)
		email_id = request.data['email_id'].lower().strip()
		name = request.data['name']
		phone_no = int(request.data['phone_no'])

		try:
			object = IntroReg.objects.get(email_id = email_id)
		except:
			object = None
		
		if object:
			return Response({'message' : 'Email already registered.'})

		else:
			participant = IntroReg()

			participant.college = college
			participant.email_id = email_id
			participant.name = name
			participant.phone_no = phone_no

			participant.save()

			data = {'status':0 , 'email_id':email_id, 'name':name, 'phone_no':phone_no}
			return Response(data)

	
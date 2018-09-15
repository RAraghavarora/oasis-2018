from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from registrations.models import Bitsian

from rest_framework_jwt.settings import api_settings

from random import choice
import string

#google oauth client side
from google.oauth2 import id_token


class Authentication(APIView):

	permission_classes = (AllowAny,)

	PASS_CHARS = string.ascii_letters + string.digits
	for i in '0oO1QlLiI':
		PASS_CHARS = PASS_CHARS.replace(i,'')

	def generate_random_password(self):
		return ''.join(choice(self.PASS_CHARS) for _ in xrange(8))

	def get_jwt(self, user):
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
		payload = jwt_payload_handler(user)
		token = jwt_encode_handler(payload)

		return token

	def post(self, request, format=None):
		try:
			is_bitsian = request.data['is_bitsian']
		except KeyError as missing:
			msg = {"message": "The following field is missing: {}".format(missing)}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

		if is_bitsian:
			try:
				token = request.data['id_token']
			except KeyError as missing:
	            msg = {"message": "The following field is missing: {}".format(missing)}
	            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

			try:
				idinfo = id_token.verify_oauth2_token(token, requests1.Request(), OAUTH_CLIENT_ID_app)
			except Exception as e:
				return Response({'message' : str(e)})

			if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
				return Response({'message': 'Invalid user'})

			email = idinfo['email']
			try:
				bitsian = Bitsian.objects.get(email=email)
			except:
				return Response({'message':'Bitsian not found.'})

			password = self.generate_random_password()
			username = email.split('@')[0]
			try:
				user = User.objects.get(username=username)
				user.email = email
				user.set_password(password)
				user.save()
			except:
				user = User.objects.create_user(username=username, password=password, email=email)
				bitsian.user = user
				bitsian.save()

			token = self.get_jwt(user)

			return Response({'token' : token})

		else:
			try:
				username = request.data['username']
				password = request.data['password']
			except:
				return Response({'message' : "Authentication credentials weren't provided"})

			try:
				print("Trying to authenticate user")
				user = authenticate(username = username, password = password)
				print(user)
			except Exception as e:
				print(e)
			
			if user is None:
				return Response({'message' : 'Incorrect Authentication credentials.'})
			
			token = self.get_jwt(user)

			return Response({'token' : token})
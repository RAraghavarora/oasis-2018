from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from registrations.models import Bitsian
from shop.models.wallet import Wallet
from shop.models.balance import Balance
from shop.permissions import TokenVerification


from random import choice
import string
from google.auth.transport import requests as google_requests

#google oauth client side
from google.oauth2 import id_token


class Authentication(APIView):

	permission_classes = (AllowAny, TokenVerification,)


	PASS_CHARS = string.ascii_letters + string.digits
	for i in '0oO1QlLiI':
		PASS_CHARS = PASS_CHARS.replace(i,'')

	CLIENT_ID_ios = "157934063064-po2m0hg1vt113ho1oohld9g06khvb74l.apps.googleusercontent.com"
	CLIENT_ID_web = "157934063064-et3fmi6jlivnr6h70q2rnegik50aqj3g.apps.googleusercontent.com"


	def generate_random_password(self):
		return ''.join(choice(self.PASS_CHARS) for _ in xrange(8))


	def get_jwt(self, user):
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
		payload = jwt_payload_handler(user)
		token = jwt_encode_handler(payload)

		return token


	def post(self, request, format=None):
		#Checks if Authentication requester if bitsian, participant or stall.
		try:
			is_bitsian = request.data['is_bitsian']
			is_stall = False
		
		except KeyError:
			try:
				is_stall = request.data['is_stall']
				is_bitsian = False
			
			except KeyError:
				msg = {"message": "Missing the identity field."}
				return Response(msg, status=status.HTTP_400_BAD_REQUEST)

		
		#Bitsian Authentication is done through Google OAuth
		if is_bitsian:
			#Checks if Google OAuth token has been provided
			#The frontend gets this token when the user logs in using Google OAuth
			try:
				token = request.data['id_token']
			
			except KeyError as missing:
				msg = {"message": "The following field is missing: {}".format(missing)}
				return Response(msg, status=status.HTTP_400_BAD_REQUEST)

			#Verifies bitsian using Google Client-Side API
			try:
				idinfo = id_token.verify_oauth2_token(token, google_requests.Request())
				if idinfo['aud'] not in [self.CLIENT_ID_web, self.CLIENT_ID_ios]:
					raise ValueError('Could not verify audience.')

			except Exception as e:
				return Response({'message' : str(e)})

			if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
				return Response({'message': 'Invalid user'})

			#Checks if Bitsian exists, return 404 if doesn't.
			email = idinfo['email']
			try:
				bitsian = Bitsian.objects.get(email=email)
				print(bitsian)
			except:
				return Response(status.HTTP_404_NOT_FOUND)

			#Checks if user exist creates if doesn't.
			username = email.split('@')[0]
			try:
				user = User.objects.get(username=username)
			
			except ObjectDoesNotExist:
				user = User.objects.create(username=username, email=email)
				bitsian.user = user
				bitsian.save()


		#Stall and Participant Authentication is done using django authentication
		else:
			#Checks for fields username and password
			try:
				username = request.data['username']
				password = request.data['password']
				print("Fetch data: ", username, password)

			except:
				msg = {'message' : "Authentication credentials weren't provided"}
				print(msg)

				return Response(msg, status = status.HTTP_400_BAD_REQUEST)

			#Authenticates the user
			try:
				user = authenticate(username = username, password = password)
				
				if user is None:
					raise User.DoesNotExist
				print("User: ", user)

			except Exception as e:
				msg = {'message' : "Incorrect Authentication Credentials or User doesn't exist"}
				return Response(msg, status = status.HTTP_404_NOT_FOUND)

		
		#Checks if wallet exists
		try:
			wallet = Wallet.objects.get(user = user)
			
			if not wallet:
				raise Wallet.DoesNotExist
			print("Wallet: ", wallet)

		except Wallet.DoesNotExist:
			msg = {'message' : 'Contact the administrators'}
			print(msg)

			return Response(msg, status = status.HTTP_400_BAD_REQUEST)
		
		#Generates the JWT Token
		token = self.get_jwt(user)

		msg = {'token' : token}
		print(msg)
		return Response(msg, status = status.HTTP_200_OK)

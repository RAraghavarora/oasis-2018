from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from registrations.models import Bitsian
from shop.models.wallet import Wallet
from shop.models.balance import Balance


from random import choice
import string

#google oauth client side
from google.oauth2 import id_token


class Authentication(APIView):

	permission_classes = (AllowAny,)

	'''
	PASS_CHARS = string.ascii_letters + string.digits
	for i in '0oO1QlLiI':
		PASS_CHARS = PASS_CHARS.replace(i,'')

	def generate_random_password(self):
		return ''.join(choice(self.PASS_CHARS) for _ in xrange(8))
	'''

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
				idinfo = id_token.verify_oauth2_token(token, requests1.Request(), OAUTH_CLIENT_ID_app)
			except Exception as e:
				return Response({'message' : str(e)})

			if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
				return Response({'message': 'Invalid user'})

			#Checks if Bitsian exists, return 404 if doesn't.
			email = idinfo['email']
			try:
				bitsian = Bitsian.objects.get(email=email)
			except:
				return Response(status.HTTP_404_NOT_FOUND)

			#Checks if user exist creates if doesn't.
			username = email.split('@')[0]
			try:
				user = User.objects.get(username=username)
			except User.DoesNotExist:
				user = User.objects.create(username=username, password=password, email=email)
				bitsian.user = user
				bitsian.save()

			#Checks if wallet exists, creates if doesn't
			try:
				wallet = Wallet.objects.get(user = request.user)
				if not wallet:
					raise Exception
			except:
				balance = Balance.objects.create()
				wallet = Wallet.objects.create(user = request.user, profile = 'B', balance=balance)
				# this bakchodi is for the signals to update to firebase
				# the balance object's str representation requires the wallet
				# so this awkward creation is needed. Refractoring it would be
				# nice
				balance = Balance.create()
				wallet.balance = balance
				wallet.save()
				balance.save()

			#Generates JWT token.
			token = self.get_jwt(user)

			return Response({'token' : token})

		#Stall and Participant Authentication is done using django authentication
		else:
			#Checks for fields username and password
			try:
				username = request.data['username']
				password = request.data['password']
			except:
				return Response({'message' : "Authentication credentials weren't provided"})

			#Authenticates the user
			try:
				user = authenticate(username = username, password = password)
			except Exception as e:
				return Response(status = status.HTTP_400_BAD_REQUEST)

			#Checks if user exists
			if user is None:
				msg = {'message' : 'Incorrect Authentication credentials.'}
				return Response(msg, status=status.HTTP_400_BAD_REQUEST)

			#Creates wallet if it doesn't exist
			try:
				wallet = user.wallet

			except Wallet.DoesNotExist:
				#Create wallet for stall, if stall exists
				if is_stall:
					try:
						stall = user.stall
					except ObjectDoesNotExist:
						msg = {'message' : 'Contact the administrators.'}
						return Response(msg, status=status.HTTP_400_BAD_REQUEST)
					balance = Balance.objects.create()
					wallet = Wallet.objects.create(user = user, profile = 'S', phone = stall.phone, balance=balance)


				#Create wallet for participant, if participant exists
				#Add a check for pcr-approved participant
				else:
					try:
						participant = user.participant
					except ObjectDoesNotExist:
						msg = {'message' : 'Contact the administrators.'}
						return Response(msg, status=status.HTTP_400_BAD_REQUEST)
					balance = Balance.objects.create()
					wallet = Wallet.objects.create(user = user, profile = 'P', phone = participant.phone, balance=balance)



			#Generates the JWT Token
			token = self.get_jwt(user)

			msg = {'token' : token}
			return Response(msg, status = status.HTTP_200_OK)

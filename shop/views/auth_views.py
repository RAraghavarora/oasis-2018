from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from registrations.models import Bitsian, Participant
from shop.models.wallet import Wallet
from shop.models.balance import Balance
from shop.permissions import TokenVerification
from shop.models.teller import Teller
from shop.models.stall import Stall
from events.models import Organization
from oasis2018.settings_config.keyconfig import CLIENT_ID_web, CLIENT_ID_ios, CLIENT_ID_android

from random import choice
import string
from google.auth.transport import requests as google_requests

#google oauth client side
from google.oauth2 import id_token


class Authentication(APIView):

	permission_classes = (TokenVerification,)


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

	@csrf_exempt
	def post(self, request, format=None):
		try:
			is_bitsian = request.data['is_bitsian']
			registration_token = request.data['registration_token']
		except KeyError as missing:
			msg = {"message": "The following field was missing: {}".format(missing)}
			return Response(msg, status=status.HTTP_400_BAD_REQUEST)

		#Bitsian Authentication
		if is_bitsian:
			try:
				token = request.data['id_token']
			except KeyError as missing:
				msg = {"message": "The following field is missing: {}".format(missing)}
				return Response(msg, status=status.HTTP_400_BAD_REQUEST)

			try:
				idinfo = id_token.verify_oauth2_token(token, google_requests.Request())
				if idinfo['aud'] not in [CLIENT_ID_web, CLIENT_ID_ios, CLIENT_ID_android]:
					raise ValueError('Could not verify audience: {}'.format(idinfo['aud']))
			except Exception as e:
				return Response({'message' : str(e)})

			if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
				return Response({'message': 'Invalid user'}, status=status.HTTP_404_NOT_FOUND)

			email = idinfo['email']
			prefix, postfix = email.split("@")
			try:
				if postfix == "pilani.bits-pilani.ac.in":
					try:
						bitsian = Bitsian.objects.get(email=email)
					except:
						user = User.objects.get_or_create(username=prefix)
						new_bitsian = Bitsian.objects.create(
														email=email,
														long_id=prefix,
														name="Bitsian",
														user=user
													)
				else:
					raise ValueError("invalid email bitsian id.")
			except Exception as e:
				msg = "Contact the administrators.".format(email)
				return Response({"message": msg}, status=status.HTTP_404_NOT_FOUND)

			username = email.split('@')[0]
			try:
				user = User.objects.get(username=username)
			except ObjectDoesNotExist:
				user = User.objects.create(username=username, email=email)
				bitsian.user = user
				bitsian.save()

			wallet, created = Wallet.objects.get_or_create(user=user, profile="B")
			balance, created = Balance.objects.get_or_create(wallet=wallet)
			if created:
				wallet.balance = balance
				wallet.save()

		#Stall and Participant Authentication
		else:
			try:
				username = request.data['username']
				password = request.data['password']
			except:
				msg = {'message' : "Authentication credentials weren't provided"}
				return Response(msg, status = status.HTTP_400_BAD_REQUEST)

			try:
				user = authenticate(username = username, password = password)
				if user is None:
					raise User.DoesNotExist
			except:
				msg = {'message' : "Incorrect Authentication Credentials."}
				return Response(msg, status = status.HTTP_404_NOT_FOUND)

			try:
				participant = user.participant
				if user.participant.firewallz_passed:
					wallet, created = Wallet.objects.get_or_create(user=user, profile="P")
					balance, created = Balance.objects.get_or_create(wallet=wallet)
					if created:
						wallet.balance = balance
						wallet.save()
				else:
					raise Exception
			except Participant.DoesNotExist:
				try:
					stall = user.stall
				except Stall.DoesNotExist:
					msg = {'message' : "Neither a Stall nor a Participant. Contact the administrators."}
					return Response(msg, status = status.HTTP_404_NOT_FOUND)
			except:
				msg = {'message' : "Participant is not firewallz passed or Something else is wrong."}
				return Response(msg, status = status.HTTP_404_NOT_FOUND)

		qr_code = user.wallet.uuid

		#Checks if wallet exists
		try:
			wallet = Wallet.objects.get(user=user)
			if not wallet:
				raise Wallet.DoesNotExist
			wallet.registration_token = registration_token
			wallet.save()
		except Wallet.DoesNotExist:
			msg = {'message' : 'Contact the administrators'}
			return Response(msg, status = status.HTTP_400_BAD_REQUEST)

		#Generates the JWT Token
		token = self.get_jwt(user)

		msg = {'user_id': user.id, 'token': token, 'qr_code': qr_code}
		return Response(msg, status = status.HTTP_200_OK)


class OrganizationsAndTellersLogin(APIView):

    def get(self, request):
        """ Let the client know which fields are required. """
        data = {"fields_required": ["username", "password"], "number_of_fields": 2}
        return Response(data)

    def post(self, request):
        """ Perform certain checks (see inline comments),
            then return a jwt for the user. """

        # first check for all keys
        try:
            username = request.data["username"]
            password = request.data["password"]
        except KeyError as missing:
            msg = {"message": "Missing the following field: \"{}\".".format(missing)}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        # check to see if such a user exists
        try:
            user = authenticate(username=username, password=password)
            if user == None:
                raise User.DoesNotExist
            try:
                user_ext = user.teller
            except Teller.DoesNotExist:
                try:
                    user_ext = user.organization
                except Organization.DoesNotExist:
                    raise User.DoesNotExist
        except User.DoesNotExist:
            return Response({"message": "Invalid/non-existant user."}, status=status.HTTP_401_UNAUTHORIZED)

        # make sure that the user is not disabled
        if user_ext.disabled:
            return Response({"message": "User has been disabled."}, status=status.HTTP_401_UNAUTHORIZED)

        # if everything checks out, then return the jwt.
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({"jwt": token, "message": "authentication successful."}, status=status.HTTP_200_OK)

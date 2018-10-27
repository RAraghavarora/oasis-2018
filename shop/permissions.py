from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from oasis2018.settings_config.keyconfig import WALLET_TOKEN

class TokenVerification(BasePermission):

	def has_permission(self, request, view):
		try:
			return request.META['HTTP_WALLET_TOKEN'] == WALLET_TOKEN
		except KeyError:
			return False

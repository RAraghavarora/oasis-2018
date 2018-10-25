from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

class TokenVerification(BasePermission):

	WALLET_TOKEN = 'asdf'

	def has_permission(self, request, view):
		try:
			return request.META['HTTP_WALLET_TOKEN'] == self.WALLET_TOKEN
		except KeyError:
			return False

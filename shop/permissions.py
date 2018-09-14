from rest_framework.permissions import BasePermission

class TokenVerification(BasePermission):

	WALLET_TOKEN = 'asdf'

	def has_permission(self, request, view):
		return request.data.get('WALLET_TOKEN') == self.WALLET_TOKEN
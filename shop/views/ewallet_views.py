from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.wallet import transferHelper
from shop.models.wallet import Wallet

### AUTH AND LOGGING REQUIRED!!!

class Transfer(APIView):
    """
        The API endpoint that will be called when money is to be transferred
        from one user's wallet to another. This view may even be called by other
        views such as the PlaceOrder view to abstract the process of
        transferring money.
    """

    def post(self, request, format=None):
        return transferHelper(request.data)

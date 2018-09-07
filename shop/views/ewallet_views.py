from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

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
        try:
            data = request.data
            try:
                source = Wallet.objects.get(id=data["source-id"])
                target = Wallet.objects.get(id=data["target-id"])
                amount = data["amount"]
            except Wallet.DoesNotExist:
                msg = {"message": "Wallet does not exist"}
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            if amount < 0:
                raise
                # log and handle accordingly
            source.transferTo(target, amount)
            msg = {"message": "successful!"}
            return Response(msg, status=status.HTTP_200_OK)
        except KeyError as missing:
            msg = {"message": "missing the following field: {}".format(missing)}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

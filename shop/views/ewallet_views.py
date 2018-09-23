from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from shop.models.wallet import Wallet
from shop.permissions import TokenVerification


class Transfer(APIView):
    """
        The API endpoint that will be called when money is to be transferred
        from one user's wallet to another. This view may even be called by other
        views such as the PlaceOrder view to abstract the process of
        transferring money.
    """

    permission_classes = (IsAuthenticated, TokenVerification,)

    def post(self, request, format=None):
            data = request.data
            try:
                source = request.user.wallet
                target_user = User.objects.get(id=data["target_user"])
                target = Wallet.objects.get(user=user)
                amount = data["amount"]
                if amount < 0:
                    return Response({"message": "transfered amount cannot be negative."}, status=status.HTTP_400_BAD_REQUEST)
                source.transferTo(target, amount, transfertype="transfer")
                msg = {"message": "successful!"}
                return Response(msg, status=status.HTTP_200_OK)
            except KeyError as missing:
                msg = {"message": "missing the following field: {}".format(missing)}
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            except Wallet.DoesNotExist:
                msg = {"message": "Wallet does not exist"}
                return Response(msg, status=status.HTTP_404_NOT_FOUND)

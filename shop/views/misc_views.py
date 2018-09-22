from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from shop.permissions import TokenVerification


class getProfile():

    permission_classes = (IsAuthenticated, TokenVerification)

    @csrf_exempt
    def post():

        # name
        # profile pic url
        # qr code string

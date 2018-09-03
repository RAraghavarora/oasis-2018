from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from shop.models.order import Order, OrderFragment

class PlaceOrder(APIView):
    """ The main view to handle orders. For the structure expected from the
        app/front-end teams, see the below """

    def post(self, request, format=None):
        data = request.data
        order = Order(customer=request.user.wallet)
        for stall in data["order"]:
            #fragment = OrderFragment(stall=Stall.objects.get())

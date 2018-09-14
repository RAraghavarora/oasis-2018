from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models.stall import Stall
from shop.models.item import Item
from shop.permissions import TokenVerification


class StallsInfo(APIView):

	permission_classes = (IsAuthenticated, TokenVerification,)

	def get(self, request):
		stalls = Stall.objects.all()
		serializer = StallSerializer(stalls, many=True)

		return Response(serializer.data)


class ProductsInfo(APIView):

	permission_classes = (IsAuthenticated, TokenVerification,)

	def get(self, request, stall_id):
		try:
			stall = Stall.objects.get()
		except Stall.DoesNotExist:
			return HttpResponse(status = 404)

		products = Item.objects.filter(itemclass__stall = stall).order_by('itemclass__name')
		serializer = ItemSerializer(products, many=True)

		return Response(serializer.data)

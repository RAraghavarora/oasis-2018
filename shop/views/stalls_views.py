from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models.stall import Stall
from shop.models.item import Item
from shop.models.order import OrderFragment
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
			stall = Stall.objects.get(id = stall_id)
		except Stall.DoesNotExist:
			return HttpResponse(status = 404)

		products = Item.objects.filter(itemclass__stall = stall).order_by('itemclass__name')
		serializer = ItemSerializer(products, many=True)

		return Response(serializer.data)


class StallOrderStatus(APIView):

	permission_classes = (IsAuthenticated, TokenVerification,)

	def post(self, request):
		try:
			order_fragment_id = request.data['order_fragment']
			order_status = request.data['order_status']
		except KeyError as missing:
			msg = {"message": "The following field is missing: {}".format(missing)}
			status = status.HTTP_400_BAD_REQUEST
			return Response(msg, status=status)

		try:
			order_fragment = OrderFragment.objects.get(id = order_fragment_id)
		except OrderFragment.DoesNotExist:
			status = status.HTTP_404_NOT_FOUND
			return Response(status = status)

		if not order_fragment.stall.user is request.user:
			msg = {"message": "Permission Denied!"}
			status = status.HTTP_401_FORBIDDEN
			return Response(msg, status)

		if not(status == "accepted" or status == "declined"):
			msg = {"message": "order_status response not recognized."}
			status = status.HTTP_400_BAD_REQUEST
			return Response(msg, status=status)

		#Stalls transfer money

		order_fragment.status = order_status
		order_fragment.save()
		return Response(status.HTTP_200_OK)


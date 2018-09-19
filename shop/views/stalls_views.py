from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models.stall import Stall
from shop.models.item import ItemClass
from shop.models.order import OrderFragment
from shop.permissions import TokenVerification
from shop.serializers import ItemClassSerializer, StallSerializer, OrderFragmentSerializer


class StallsList(APIView):

	permission_classes = (IsAuthenticated, TokenVerification,)

	#Return Stalls list, including name and description of each stall.
	def get(self, request):
		stalls = Stall.objects.all()
		serializer = StallSerializer(stalls, many=True)

		return Response(serializer.data, status = status.HTTP_200_OK)


class ProductsList(APIView):

	permission_classes = (IsAuthenticated, TokenVerification,)

	#Return Products list, corresponding to thhe stall stall_id.
	def get(self, request, stall_id):
		try:
			stall = Stall.objects.get(id = stall_id)
		except Stall.DoesNotExist:
			msg = {'message' : 'Stall does not exist.'}
			return Response(msg, status = status.HTTP_404_NOT_FOUND)

		products = stall.menu.all()
		serializer = ItemClassSerializer(products, many=True)

		return Response(serializer.data, status = status.HTTP_200_OK)


class StallOrdersList(APIView):

	permission_classes = (IsAuthenticated, TokenVerification,)

	#Return list of all Orders
	#Update to return list of pending orders
	def get(self, request):
		try:
			stall = request.user.stall
			if stall is None:
				raise Exception
		except:
			status = status.HTTP_401_UNAUTHORIZED
			return Response(status = status)

		orders = stall.orders.all().order_by('orders__order__timestamp')
		serializer = OrderFragmentSerializer(orders, many = True)

		return Response(serializer.data, status = status.HTTP_200_OK)


class StallOrderStatus(APIView):

	permission_classes = (IsAuthenticated, TokenVerification,)

	#Accepts stall's response to OrderFragment
	def post(self, request):
		try:
			order_fragment_id = request.data['order_fragment']
			order_status = request.data['order_status']
		except KeyError as missing:
			msg = {"message": "The following field is missing: {}".format(missing)}
			return Response(msg, status = status.HTTP_400_BAD_REQUEST)

		try:
			order_fragment = OrderFragment.objects.get(id = order_fragment_id)
		except OrderFragment.DoesNotExist:
			return Response(status = status.HTTP_404_NOT_FOUND)

		if not order_fragment.stall.user is request.user:
			msg = {"message": "Permission Denied!"}
			return Response(msg, status = status.HTTP_403_FORBIDDEN)

		if not(status == "accepted" or status == "declined"):
			msg = {"message": "order_status response not recognized."}
			return Response(msg, status = status.HTTP_400_BAD_REQUEST)

		#Stalls transfer money

		order_fragment.status = order_status
		order_fragment.save()
		return Response(status.HTTP_200_OK)

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

from firebase_admin import firestore, messaging

import datetime

class StallsList(APIView):

	permission_classes = (TokenVerification,)

	#Return Stalls list, including name and description of each stall.
	def get(self, request):
		stalls = Stall.objects.all()
		serializer = StallSerializer(stalls, many=True)

		return Response(serializer.data, status = status.HTTP_200_OK)


class ProductsList(APIView):

	permission_classes = (TokenVerification,)

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
			return Response(status = status.HTTP_401_UNAUTHORIZED)

		orders_pending = OrderFragment.objects.filter(stall = stall, status = OrderFragment.PENDING).order_by('order__timestamp')
		orders_accepted = OrderFragment.objects.filter(stall = stall, status = OrderFragment.ACCEPTED).order_by('order__timestamp')
		orders_ready = OrderFragment.objects.filter(stall = stall, status = OrderFragment.READY).order_by('order__timestamp')
		orders_finished = OrderFragment.objects.filter(stall = stall, status = OrderFragment.FINISHED).order_by('order__timestamp')

		serializer_pending = OrderFragmentSerializer(orders_pending, many = True)
		serializer_accepted = OrderFragmentSerializer(orders_accepted, many = True)
		serializer_ready = OrderFragmentSerializer(orders_ready, many = True)
		serializer_finished = OrderFragmentSerializer(orders_finished, many = True)

		serializer_data = {
			"pending" : serializer_pending.data,
			"accepted" : serializer_accepted.data,
			"finished" : serializer_finished.data,
			"ready" : serializer_ready.data
		}

		return Response(serializer_data, status = status.HTTP_200_OK)


class StallOrderStatus(APIView):

	permission_classes = (IsAuthenticated, TokenVerification,)

	status_dict = {long_form : short_form for short_form, long_form in OrderFragment.STATUS}
	status_responses = ["Accepted", "Declined", "Ready", "Finished"]

	# def sendNotification(self, pk, registration_token, order_status):
	# 	title = 'Order Status: {}'.format(order_status)
	# 	body = 'This is a notification.'

	# 	db = firestore.client()
	# 	data = {
	# 		"title" : title,
	# 		"body" : body
	# 	}

	# 	col_str = "User #{}".format(pk)
	# 	collection = db.collection(col_str)
	# 	doc_string = "Notifications"
	# 	doc_ref = collection.document(doc_string)
	# 	doc_ref.set({
	# 		str(datetime.datetime.now()) : str(data)
	# 	})

	# 	message = messaging.Message(
	# 	    notification = messaging.Notification(
	# 	        title = title,
	# 	        body = body,
	# 	    ),
	# 	    token = registration_token,
	# 	)
	# 	try:
	# 		response = messaging.send(message)
	# 		print(response)

	# 	except Exception as e:
	# 		print(e)


	#Accepts stall's response to OrderFragment
	def post(self, request):
		try:
			order_fragment = OrderFragment.objects.get(id = request.data['order_fragment'])
			order_status = request.data['order_status'].title()
		except KeyError as missing:
			msg = {"message": "The following field is missing: {}".format(missing)}
			return Response(msg, status = status.HTTP_400_BAD_REQUEST)
		except OrderFragment.DoesNotExist:
			msg = {"message" : "Order Fragment doesn't exist."}
			return Response(status = status.HTTP_404_NOT_FOUND)
		except Exception:
			msg = {"message" : "Something seems to have gone wrong."}
			return Response(status = status.HTTP_400_BAD_REQUEST)

		if not order_fragment.stall.user == request.user:
			msg = {"message": "Permission Denied!"}
			return Response(msg, status = status.HTTP_403_FORBIDDEN)

		if not order_status in self.status_responses:
			msg = {"message": "order_status response not recognized."}
			return Response(msg, status = status.HTTP_400_BAD_REQUEST)

		# try:
		# 	registration_token = order_fragment.order.customer.registration_token
		# 	pk = order_fragment.order.customer.id
		# except:
		# 	pass
		# self.sendNotification(pk, registration_token, order_status)

		#Money transferred to Stalls
		if order_status == 'Finished':
			request.user.wallet.balance.add(transfers = order_fragment.calculateSubTotal())

		order_fragment.status = self.status_dict[order_status]

		order_fragment.save()
		msg = {"message" : "Request Successful"}
		return Response(msg, status = status.HTTP_200_OK)
		

class SwitchItemAvailability(APIView):

	permission_classes = (IsAuthenticated, TokenVerification)

	def post(self, request):
		try:
			item_id = request.data["item_id"]
			available = request.data["available"]
			item = ItemClass.objects.get(pk = item_id)
		except KeyError as missing:
			msg = {"message" : "The following field was missing: {}".format(missing)}
			return Response(msg, status = status.HTTP_400_BAD_REQUEST)
		except ItemClass.DoesNotExist:
			msg = {"message" : "Item doesn't exist."}
			return Response(msg, status = status.HTTP_404_NOT_FOUND)

		try:
			stall = request.user.stall
			print(stall)
			print(item.stall)
			if not item.stall == stall:
				raise Exception
		except:
			msg = {"message" : "Restricted Access."}
			return Response(msg, status = status.HTTP_403_FORBIDDEN)

		item.is_available = available
		item.save()

		msg = {"message" : "Request Successful!"}
		return Response(msg, status = status.HTTP_200_OK)


class SwitchStall(APIView):

	def post(self, request):
		try:
			available = request.data["available"]
			stall = request.user.stall
		except KeyError as missing:
			msg = {"message" : "The following field was missing: {}".format(missing)}
			return Response(msg, status = status.HTTP_400_BAD_REQUEST)

		items = stall.menu.all()
		for item in items:
			item.is_available = available
			item.save()

		msg = {"message" : "Request Succesful"}
		return Response(msg, status = status.HTTP_200_OK)
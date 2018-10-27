 # -*- coding: utf-8 -*-
# from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.shortcuts import render
# from registrations.models import *
#from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from ems.models import *
# from django.contrib.auth.models import User
# from registrations.models import *
# from shop.models import *
# from api.serializers import *
# from apogee2018.keyconfig import *
from django.views.decorators.csrf import csrf_exempt
# import sendgrid
# import os
# from sendgrid.helpers.mail import *
# from django.contrib.auth.decorators import login_required
# import re
# import requests
# from rest_framework.decorators import api_view, permission_classes, authentication_classes
# from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
# from rest_framework.authentication import BasicAuthentication, SessionAuthentication
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# from instamojo_wrapper import Instamojo
# from shop.views import create_wallet
# from google.oauth2 import id_token
# from google.auth.transport import requests as oauth_requests
# try:
# 	from apogee2018.config import *
# 	from apogee2018.keyconfig import *
# 	api = Instamojo(api_key=INSTA_API_KEY, auth_token=AUTH_TOKEN)
# except:
# 	api = Instamojo(api_key=INSTA_API_KEY_test, auth_token=AUTH_TOKEN_test, endpoint='https://test.instamojo.com/api/1.1/') #when in development

# from django.core.cache import cache
# import uuid
# import time
# import pyrebase
# import os
# from apogee2018.settings import BASE_DIR
# from django.contrib import messages
# import random
# from django.db.models import Q
# import string
# from random import choice
# chars = string.letters + string.digits
# for i in '0oO1QlLiI':
#     chars = chars.replace(i,'')
# import random
# import os
# config = {
#     "apiKey": "AIzaSyCkehNgOS7oZ4oE5JNnNR7LDfY4wqDxQW0",
#     "authDomain": "vendorapp-80efa.firebaseio.com",
# 	"databaseURL": "https://vendorapp-80efa.firebaseio.com",
#     "storageBucket": "vendorapp-80efa.appspot.com",
# 	"serviceAccount": os.path.join(BASE_DIR, "apogee2018/vendorapp-80efa-firebase-adminsdk-ub973-3f154fa44d.json")
# }
# firebase = pyrebase.initialize_app(config)
# db = firebase.database()
USER_NAMES = ['f20170636', 'f2015831', 'f20170216', 'f2016023', 'f20170647']
def home(request):
	return render(request, 'storewebapp/login.html', )

@csrf_exempt
def bitsian_login(request):
	# if not request.user.is_authenticated():
	# 	if request.method == 'POST':
	# 		token = request.POST['id_token']
	# 		idinfo = id_token.verify_oauth2_token(token, oauth_requests.Request(), OAUTH_CLIENT_ID)

	# 		if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
	# 			context = {
	# 					'error_heading': "Invalid user.",
	# 					'message': "Sorry! Your user hasn't been activated yet.",
	# 					'url':request.build_absolute_uri(reverse('storewebapp:home'))
	# 					}
	# 			return render(request, 'storewebapp/message.html', context)
	# 		email = idinfo['email']
	# 		username = email.split('@')[0]
	# 		try:
	# 			bitsian = Bitsian.objects.filter(email=email)[0]
	# 			bitsian_serializer = BitsianSerializer(bitsian)
	# 			print 'Got bitsian'
	# 		except:
	# 			context = {
	# 					'error_heading': "Bitsian not found.",
	# 					'message': "Sorry! Bitsian not found yet.",
	# 					'url':request.build_absolute_uri(reverse('storewebapp:home'))
	# 					}
	# 			return render(request, 'storewebapp/message.html', context)
	# 		try:
	# 			user = User.objects.get(username=username)
	# 			user.email = email
	# 			user.save()
	# 			bitsian.user = user
	# 			bitsian.save()
	# 			login(request, user)
	# 			return redirect('storewebapp:home')
	# 		except:
	# 			username = email.split('@')[0]
	# 			password = ''.join(choice(chars) for _ in xrange(8))
	# 			user, created = User.objects.get_or_create(username=username,email=bitsian.email)
	# 			user.set_password(password)
	# 			user.save()
	# 			user = authenticate(username=username, password=password)
	# 			if user.is_active:
	# 				login(request, user)
	# 				return redirect('storewebapp:home')
	# 			else:
	# 				context = {
	# 					'error_heading': "Inactive user",
	# 					'message': "Sorry! Your user hasn't been activated yet.",
	# 					'url':request.build_absolute_uri(reverse('storewebapp:home'))
	# 					}
	# 				return render(request, 'storewebapp/message.html', context)
	# 	else:
	# 		return render(request, 'storewebapp/bitsian_login.html')
	# user = request.user
	# try:
	# 	bitsian = Bitsian.objects.get(email=request.user.email)
	# except:
	# 	logout(request)
	# 	context = {
	# 					'error_heading': "Bitsian not found.",
	# 					'message': "Sorry! Bitsian not found yet.",
	# 					'url':request.build_absolute_uri(reverse('storewebapp:home'))
	# 					}
	# 	return render(request, 'storewebapp/message.html', context)
		
	# try:
	# 	wallet = Wallet.objects.get(bitsian=bitsian)
	# except:
	# 	wallet = create_wallet(user, 9898989898, True)
	# 	wallet.is_bitsian = True
	# 	wallet.save()
	# try:
	# 	cart = Cart.objects.get(bitsian=bitsian)
	# except:
	# 	cart = Cart.objects.create(bitsian=bitsian, is_bitsian=True, user=user)
	# wallet_serializer = WalletSerializer(wallet)
	# cart_serializer = CartSerializer(cart)
	# stall_rows = [{'data':[stall.name], 'link':[{'title':'View Items','url':reverse('storewebapp:get_products', kwargs={'stall_id':stall.id})}]} for stall in Stall.objects.all()]
	# stall_headings = ['Stall Name', 'View Items']
	# stall_title = 'Order Here'
	# stall_table = {'rows':stall_rows, 'headings':stall_headings, 'title':stall_title}
	# sg_list = StallGroup.objects.filter(user=user).exclude(stall__name__icontains='ProfShow')
	# db = firebase.database()
	# list_ = {}
	# for t in wallet.transactions.all():
	# 	list_[t.id] = TransactionSerializer(t).data
	# dict_ = {'wallet':wallet_serializer.data, 'transactions': list_}
	# ts = TransactionSerializer(wallet.transactions.all(), many=True).data
	# db.child('wallet').child(wallet.uid).set(dict_)
	# # print wallet_serializer.data['']
	# return render(request, 'storewebapp/profile.html', {'tables':[stall_table,],'participant':bitsian, 'wallet':wallet, 'sg_list':sg_list})
	return render(request,'storewebapp/bitsian_login.html')

def get_status(sg):
	if sg.order_ready:
		return "Order Ready"
	else:
		return "Order on the way."

def profile(request):
    return render(request, 'storewebapp/profile.html', )

# def participant_login(request):
# 	if not request.user.is_authenticated():
# 		if request.method == 'POST':
# 			username = request.POST['username']
# 			password = request.POST['password']
# 			user = authenticate(username=username, password=password)
# 			if user is not None:
# 				if user.is_active:
# 					# if not user.participant.email_verified:
# 					# 	context = {'error_heading' : "Email not verified",
# 					# 	'message' :  'It seems you haven\'t verified your email yet. Please verify it as soon as possible to proceed.',
# 					# 	'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 					# 	return render(request, 'storewebapp/message.html', context)
# 					login(request, user)
# 				else:
# 					context = {'error_heading' : "Account Inactive", 'message' :  'Your account is currently INACTIVE. To activate it, call the following members of the Department of Publications and Correspondence. Alanckrit Jain: %s - pcrapogee@bits-apogee.org .'%(get_pcr_number()), 'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 					return render(request, 'storewebapp/message.html', context)
# 			else:
# 				messages.warning(request,'Invalid login credentials')
# 				return redirect(request.META.get('HTTP_REFERER'))
# 		else:
# 			return render(request, 'storewebapp/login.html')
# 	user = request.user
# 	try:
# 		participant = Participant.objects.get(user=request.user)
# 	except:
# 		bitsian = Bitsian.objects.get(user=request.user)
# 		return redirect('storewebapp:bitsian_login')
# 	if not participant.firewallz_passed:
# 		logout(request)
# 		context = {'error_heading' : "Not passed firewallz",
# 				'message' :  'Access denied.',
# 				'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 		return render(request, 'storewebapp/message.html', context)
# 	event_set = [participation.event for participation in Participation.objects.filter(participant=participant, pcr_approved=True)]
# 	event_serializer = EventSerializer(event_set, many=True)
# 	try:
# 		wallet = Wallet.objects.get(participant=participant)
# 	except:
# 		wallet = create_wallet(request.user, participant.phone, False)
# 	try:
# 		cart = Cart.objects.get(participant=participant)
# 	except:
# 		cart = Cart.objects.create(participant=participant, user=request.user)
# 	wallet_serializer = WalletSerializer(wallet)
# 	stall_rows = [{'data':[stall.name], 'link':[{'title':'View Items','url':reverse('storewebapp:get_products', kwargs={'stall_id':stall.id})}]} for stall in Stall.objects.all()]
# 	stall_headings = ['Stall Name', 'View Items']
# 	stall_title = 'Order Here!'
# 	stall_table = {'rows':stall_rows, 'headings':stall_headings, 'title':stall_title}
# 	sg_list = StallGroup.objects.filter(user=user).exclude(stall__name__icontains='ProfShow')
# 	list_ = {}
# 	for t in wallet.transactions.all():
# 		list_[t.id] = TransactionSerializer(t).data
# 	dict_ = {'wallet':wallet_serializer.data, 'transactions': list_}
# 	ts = TransactionSerializer(wallet.transactions.all(), many=True).data
# 	db.child('wallet').child(wallet.uid).set(dict_)
# 	print wallet.userid
# 	return render(request, 'storewebapp/profile.html', {'tables':[stall_table,], 'sg_list':sg_list,'participant':participant, 'wallet':wallet})

def get_stall_status(sg):
	if sg.order_ready:
		return 'Order Ready'
	else:
		return 'Pending'

def prof_show_details(request):
    return render(request, 'storewebapp/prof_show_details.html')

# @login_required
# def prof_show_details(request):
#     user = request.user
#     try:
#         bitsian = Bitsian.objects.get(email=user.email)
#         attendance_list =  Attendance.objects.filter(bitsian=bitsian)
#     except:
#         try:
#             participant = Participant.objects.get(user=user)    
#             attendance_list = Attendance.objects.filter(participant=participant)
#         except:
#             return HttpResponseRedirect('https://bits-apogee.org')
#     return render(request, 'storewebapp/prof_show_details.html', {'attendance_list':attendance_list})

#@login_required
def add_money(request):
	#user = request.user
	#try:
		#bitsian = Bitsian.objects.get(email=request.user.email)
		#bitsian = True
	#except:
		#bitsian = False
	return render(request, 'storewebapp/add_money.html' )

# @login_required
# def add_money_request(request):
# 	# user = request.user
# 	# username = user.username
# 	# if username not in USER_NAMES:
# 	context = {'error_heading' : "Wait",
# 					'message' :  'APOGEE chhodo Midsem aa rhe hain!! Padh lo',
# 					'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 	return render(request, 'storewebapp/message.html', context)
# 	user = request.user
# 	try:
# 		wallet = Wallet.objects.get(user=user)
# 	except:
# 		context = {'error_heading' : "Payment Error.",
# 					'message' :  'Wallet does not exist.',
# 					'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 		return render(request, 'storewebapp/message.html', context)
# 	data = request.POST
# 	try:
# 		amount = int(data['amount'])
# 		if amount <= 0 or amount >10000:
# 			raise Exception
# 	except:
# 		messages.warning(request,'Enter a valid amount')
# 		return redirect(request.META.get('HTTP_REFERER'))
# 	try:
# 		t_type = data['type']
# 		if t_type == "swd":
# 			transaction = Transaction(value=amount, wallet=wallet, t_type="swd")
# 			transaction.save()
# 			wallet.curr_balance += amount
# 			wallet.save()
# 			db = firebase.database()
# 			db.child('wallet').child(wallet.uid).child('transactions').child(transaction.id).set(TransactionSerializer(transaction).data)
# 			db.child('wallet').child(wallet.uid).child('wallet').set(WalletSerializer(wallet).data)
# 			context = {'error_heading' : "Payment Successful.",
# 						'message' :  'Payment completed',
# 						'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 			return render(request, 'storewebapp/message.html', context)
# 		else:
# 			raise Exception
# 	except:
# 		pass
# 	try:
# 		amount = int(data['amount'])
# 		if amount <= 0:
# 			raise Exception
# 	except:
# 		messages.warning(request,'Enter a valid amount')
# 		return redirect(request.META.get('HTTP_REFERER'))
# 	purpose = 'Add Money to the Apogee wallet'
# 	phone = int(wallet.phone)
# 	try:
# 		part = user.participant
# 		name = part.name
# 		email = part.email
# 	except:
# 		email = user.email
# 		bitsian = Bitsian.objects.get(email=email)
# 		name = user.get_full_name()

# 	redirect_url = request.build_absolute_uri(reverse("storewebapp:add_money_response"))
# 	response = api.payment_request_create(buyer_name=name, email=email, amount=amount, purpose=purpose, phone=phone, redirect_url=redirect_url)
# 	try:
# 		url = response['payment_request']['longurl']
# 		return HttpResponseRedirect(url)
# 	except:
# 		context = {'error_heading' : "Payment Error.",
# 					'message' :  'Payment could not be initialised',
# 					'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 		return render(request, 'storewebapp/message.html', context)

# def add_money_response(request):
# 	payid=str(request.GET['payment_request_id'])
# 	try:
# 		headers = {'X-Api-Key': INSTA_API_KEY, 'X-Auth-Token': AUTH_TOKEN}
#    		r = requests.get('https://www.instamojo.com/api/1.1/payment-requests/'+str(payid),headers=headers)
# 	except:
# 		headers = {'X-Api-Key': INSTA_API_KEY_test, 'X-Auth-Token': AUTH_TOKEN_test}
# 		r = requests.get('https://test.instamojo.com/api/1.1/payment-requests/'+str(payid), headers=headers)    ### when in development

# 	json_ob = r.json()
# 	if (json_ob['success']):
# 		payment_request = json_ob['payment_request']
# 		purpose = payment_request['purpose']
# 		amount = int(float(payment_request['amount']))
# 		email = payment_request['email']
# 		try:
# 			bitsian = Bitsian.objects.get(email=email)
# 			wallet = bitsian.wallet
# 		except:
# 			part = Participant.objects.get(email=email)
# 			wallet = part.wallet
# 		payment_id = payment_request['payments'][0]['payment_id']
# 		try:
# 			transaction = Transaction.objects.get(payment_refund_id=payment_id,)
# 			return HttpResponse('Payment Unsuccessful')
# 		except:
# 			pass
# 		transaction = Transaction.objects.create(value=amount, wallet=wallet, payment_refund_id=payment_id, t_type="add")
# 		wallet.curr_balance += amount
# 		wallet.save()
# 		db = firebase.database()
# 		db.child('wallet').child(wallet.uid).child('transactions').child(transaction.id).set(TransactionSerializer(transaction).data)
# 		db.child('wallet').child(wallet.uid).child('wallet').set(WalletSerializer(wallet).data)
# 		context = {'error_heading' : "Payment Successful.",
#                     'message' :  'Payment completed',
#                     'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 		return render(request, 'storewebapp/message.html', context)
# 	context = {'error_heading' : "Payment Unsuccessful.",
#                     'message' :  'Payment incomplete',
#                     'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 	return render(request, 'storewebapp/message.html', context)

# @csrf_exempt
def send_money(request):
	return render(request, 'storewebapp/send_money.html')

# @login_required
# def transfer_money(request):
# 	# user = request.user
# 	# username = user.username
# 	# if username not in USER_NAMES:
# 	context = {'error_heading' : "Wait",
# 					'message' :  'APOGEE chhodo Midsem aa rhe hain!! Padh lo',
# 					'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 	return render(request, 'storewebapp/message.html', context)
# 	data = request.POST
# 	user = request.user
# 	try:
# 		wallet = user.wallet
# 	except:
# 		context = {'error_heading' : "Payment Error.",
# 					'message' :  'Wallet does not exist.',
# 					'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 		return render(request, 'storewebapp/message.html', context)
# 	try:
# 		userid = request.POST['user_id']
# 		wallet_rec = Wallet.objects.get(userid=userid)
# 		user_rec = wallet_rec.user
# 	except:
# 		messages.warning(request,'Invalid Code for the user')
# 		return redirect(request.META.get('HTTP_REFERER'))
# 	try:
# 		amount = int(request.POST['amount'])
# 		if amount<=0:
# 			raise Exception
# 	except:
# 		messages.warning(request,'Invalid Amount')
# 		return redirect(request.META.get('HTTP_REFERER'))
# 	if amount > wallet.curr_balance:
# 		messages.warning(request,'Insufficient Balance')
# 		return redirect(request.META.get('HTTP_REFERER'))
# 	if wallet == wallet_rec:
# 		messages.warning(request,'Cannot be done.')
# 		return redirect(request.META.get('HTTP_REFERER'))
# 	wallet.curr_balance = wallet.curr_balance - amount
# 	wallet.save()
# 	wallet_rec.curr_balance = wallet_rec.curr_balance + amount
# 	wallet_rec.save()
# 	transaction = Transaction.objects.create(wallet=wallet, value = -amount, t_type="transfer", transfer_to_from=wallet_rec)
# 	db.child('wallet').child(wallet.uid).child('transactions').child(transaction.id).set(TransactionSerializer(transaction).data)
# 	db.child('wallet').child(wallet.uid).child('wallet').set(WalletSerializer(wallet).data)
# 	transaction_rec = Transaction.objects.create(wallet=wallet_rec, value = amount, t_type="recieve", transfer_to_from=wallet)
# 	db.child('wallet').child(wallet_rec.uid).child('transactions').child(transaction_rec.id).set(TransactionSerializer(transaction_rec).data)
# 	db.child('wallet').child(wallet_rec.uid).child('wallet').set(WalletSerializer(wallet_rec).data)
# 	context = {'error_heading' : "Transfer Successful.",
#                     'message' :  'Transfer successful to %s'%user_rec.username,
#                     'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 	return render(request, 'storewebapp/message.html', context)

# @login_required
# def show_transactions(request):
# 	user = request.user
# 	transactions = []
# 	cancelled_transactions = []
# 	for transaction in Transaction.objects.filter(wallet__user=user):
# 		try:
# 			stall_group = StallGroup.objects.get(transaction=transaction)
# 			if stall_group.cancelled:
# 				cancelled_transactions.append(transaction)
# 			else:
# 				raise Exception
# 		except:
# 			transactions.append(transaction)
# 	rows = [{'data':[transaction.t_type, transaction.value], 'link':[{'title':'View Details', 'url':reverse('storewebapp:transaction_details', kwargs={'t_id':transaction.id})}]} for transaction in transactions]
# 	headings = ['Type', 'Amount', 'View Details']
# 	title = 'Transaction Details'
# 	table = {
# 		'rows':rows,
# 		'headings':headings,
# 		'title':title
# 	}
# 	rows = [{'data':[transaction.t_type, transaction.value], 'link':[{'title':'View Details', 'url':reverse('storewebapp:transaction_details', kwargs={'t_id':transaction.id})}]} for transaction in cancelled_transactions]
# 	headings = ['Type', 'Amount', 'View Details']
# 	title = 'Cancelled Transaction Details'
# 	c_table = {
# 		'rows':rows,
# 		'headings':headings,
# 		'title':title
# 	}
# 	return render(request, 'storewebapp/tables.html', {'tables':[table, c_table]})

def show_transactions(request):
	return render(request, 'storewebapp/past_transactions.html')

# @login_required
# def transaction_details(request, t_id):
# 	transaction = Transaction.objects.get(id=t_id)
# 	if not transaction.wallet.user == request.user:
# 		context = {'error_heading' : "Access Denied",
# 					'message' :  'Illegal Access.',
# 					'url':request.build_absolute_uri(reverse('storewebapp:show_transactions'))}
# 		return render(request, 'storewebapp/message.html', context)
# 	if str(transaction.t_type) == 'buy':
# 		stall_group = StallGroup.objects.get(transaction=transaction)
# 		rows = [{'data':[get_product_name(sale.product), sale.product.price,sale.quantity], 'link':[]} for sale in stall_group.sales.all()]
# 		headings = ['Product', 'Price/Item ','Quantity']
# 		title = 'Items bought under transaction'
# 		table = {
# 			'rows':rows,
# 			'headings':headings,
# 			'title':title
# 		}
# 	elif str(transaction.t_type) == 'add':
# 		return redirect('storewebapp:show_transactions')
# 	elif str(transaction.t_type) == 'swd':
# 		return redirect('storewebapp:show_transactions')
# 	elif str(transaction.t_type) == 'transfer':
# 		rec_wallet = transaction.transfer_to_from
# 		if rec_wallet.is_bitsian:
# 			bitsian = rec_wallet.bitsian
# 			rows = [{'data':[rec_wallet.bitsian.name, rec_wallet.bitsian.email], 'link':[]}]
# 			headings = ['Name of receiver', 'Email']
# 		else:
# 			participant = rec_wallet.participant
# 			rows = [{'data':[rec_wallet.participant.name, rec_wallet.participant.email, participant.phone], 'link':[]}]
# 			headings = ['Name of receiver', 'Email', 'Phone']
# 		title = 'Transaction of Rs ' + str(transaction.value) + 'at ' + str(transaction.created_at)
# 		table = {
# 			'rows':rows,
# 			'headings':headings,
# 			'title':title
# 		}
# 	elif str(transaction.t_type) == 'recieve': ##### Tushar is tooo weak with spellings
# 		rec_wallet = transaction.transfer_to_from
# 		if rec_wallet.is_bitsian:
# 			bitsian = rec_wallet.bitsian
# 			rows = [{'data':[rec_wallet.bitsian.name, rec_wallet.bitsian.email], 'link':[]}]
# 			headings = ['Name of giver', 'Email']
# 		else:
# 			participant = rec_wallet.participant
# 			rows = [{'data':[rec_wallet.participant.name, rec_wallet.participant.email, participant.phone], 'link':[]}]
# 			headings = ['Name of giver', 'Email', 'Phone']
# 		title = 'Transaction of Rs ' + str(transaction.value) + ' at ' + str(transaction.created_at)
# 		table = {
# 			'rows':rows,
# 			'headings':headings,
# 			'title':title
# 		}
# 	else:
# 		context = {'error_heading' : "Access Denied",
#                     'message' :  'Illegal Access.',
#                     'url':request.build_absolute_uri(reverse('storewebapp:show_transactions'))}
# 		return render(request, 'storewebapp/message.html', context)
# 	return render(request, 'storewebapp/tables.html', {'tables':[table,], 'time':transaction.created_at})

# def get_product_name(obj):
# 	a_name = obj.product.name
# 	if not obj.size.name == 'NA':
# 		a_name += (' ' + obj.size.name)
# 	if not obj.product.colour.name == 'NA':
# 		a_name += (' ' + obj.product.colour.name)
# 	if not obj.product.if_veg is None:
# 		is_veg = obj.product.if_veg
# 		if is_veg:
# 			a_name += "(Veg)"
# 		else:
# 			a_name += "(NonVeg)"
# 	return a_name

# @login_required
# def get_stalls(request):
# 	stalls = Stall.objects.all()
# 	rows = [{'data':{'name':stall.name, 'description':stall.description, }, 'link':[{'title':'View Items', 'url':reverse('storewebapp:get_products', kwargs={'stall_id':stall.id})}]} for stall in Stall.objects.all()]
# 	headings = ['Stall Name', 'Description', 'View Items']
# 	title = 'Stall List'
# 	return render(request, 'storewebapp/tables.html', {'tables':[{'rows': rows, 'headings':headings, 'title':title}]})

def stalls(request, stall_id):
    return render(request, 'storewebapp/add_products.html')

# @login_required
# def get_products(request, stall_id):
# 	stall = get_object_or_404(Stall,id=stall_id)
# 	cart = Cart.objects.get(user=request.user)
# 	products = []
# 	for prod in stall.menu.all():
# 		for mainprod in prod.mainproducts.filter(is_available=True):
# 			products.append(mainprod)
# 	return render(request, 'storewebapp/add_products.html', {'products':products, 'stall':stall, 'cart':cart})

# @login_required
# def get_sg_products(request, sg_id):
#     stall_group = get_object_or_404(StallGroup, id=sg_id)
#     if not stall_group.user == request.user:
#         context = {'error_heading' : "Access denied",
#                     'message' :  'Invalid Access.',
#                     'url':request.build_absolute_uri(reverse('storewebapp:home'))}
#         return render(request, 'storewebapp/message.html', context)
#     rows = [{'data':[get_product_name(sale.product), sale.quantity], 'link':[]} for sale in stall_group.sales.all()]
#     headings = ['Product', 'Quantity']
#     title = 'Items bought from %s'%(stall_group.stall.name)
#     table = {
#         'rows':rows,
#         'headings':headings,
#         'title':title
#     }
#     return render(request, 'storewebapp/tables.html', {'tables':[table,]})

# @login_required
# def add_to_cart(request, stall_id):
# 	stall = get_object_or_404(Stall,id=stall_id)
# 	products = []
# 	cart = Cart.objects.get(user=request.user)
# 	for prod in stall.menu.all():
# 		for mainprod in prod.mainproducts.filter(is_available=True):
# 			products.append(mainprod)
# 	data = request.POST
# 	for product in products:
# 		try:
# 			if data[str(product.id)] == '':
# 				continue
# 			quantity = int(data[str(product.id)])
# 			if quantity < 0:
# 				raise Exception
# 		except:
# 			context = {'error_heading' : "Invalid input.",
# 						'message' :  'Invalid quantity input for %s'%product.product.name,
# 					'url':request.build_absolute_uri(reverse('storewebapp:get_products', kwargs={"stall_id":stall.id}))}
# 			return render(request, 'storewebapp/message.html', context)
# 		if quantity > product.quantity:
# 			context = {'error_heading' : "Invalid input.",
# 						'message' :  'Not enough quantity for %s'%product.product.name,
# 					'url':request.build_absolute_uri(reverse('storewebapp:get_products', kwargs={"stall_id":stall.id}))}
# 			return render(request, 'storewebapp/message.html', context)
# 		try:
# 			sale = Sale.objects.get(cart=cart, product=product)
# 			sale.quantity += quantity
# 			cart.amount += ((product.price)*quantity)
# 			sale.save()
# 		except:
# 			if quantity>0:
# 				Sale.objects.create(cart=cart, product=product, quantity=quantity)
# 				cart.amount += ((product.price)*quantity)
# 			else:
# 				pass
# 	cart.save()
# 	return redirect('storewebapp:view_cart')

# @login_required
# def view_cart(request):
# 	cart = Cart.objects.get(user=request.user)
# 	if request.method == 'POST':
# 		data = request.POST
# 		try:
# 			sale_list = Sale.objects.filter(id__in=data.getlist('sale_list'))
# 		except:
# 			return redirect(request.META.get('HTTP_REFERER'))
# 		for sale in sale_list:
# 			if not sale.cart.user == request.user:
# 				continue
# 			product = sale.product
# 			quantity = sale.quantity
# 			cart.sales.remove(sale)
# 			cart.amount -= (product.price*quantity)
# 		cart.save()
# 	sale_list = Sale.objects.filter(cart=cart)
# 	return render(request, 'storewebapp/view_cart.html', {'sale_list':sale_list, 'cart':cart})

def view_cart(request):
	return render(request, 'storewebapp/view_cart.html')

# @login_required
# def checkout_payment(request):
# 	# user = request.user
# 	# username = user.username
# 	# if username not in USER_NAMES:
# 	context = {'error_heading' : "Wait",
# 					'message' :  'APOGEE chhodo Midsem aa rhe hain!! Padh lo',
# 					'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 	return render(request, 'storewebapp/message.html', context)

# 	try:
# 		user = request.user
# 		wallet = user.wallet
# 		curr_balance = wallet.curr_balance
# 		cart = user.cart
# 	except:
# 		context = {'error_heading' : "Invalid access",
#                     'message' :  'Wallet does not exist',
#                     'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 		return render(request, 'storewebapp/message.html', context)
# 	stall_set = []
# 	sales = cart.sales.all()
# 	if not sales:
# 		context = {'error_heading' : "Cart is empty",
#                     'message' :  'Please add some products to cart',
#                     'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 		return render(request, 'storewebapp/message.html', context)
# 	total = 0
# 	for sale in sales:
# 		product = sale.product
# 		if not product.is_available:
# 			context = {'error_heading' : "Item not available",
# 	                    'message' :  product.__unicode__() + ' is not available right now. Remove this from cart and then checkout',
# 	                    'url':request.build_absolute_uri(reverse('storewebapp:view_cart'))}
# 			return render(request, 'storewebapp/message.html', context)

# 		total += (product.price*sale.quantity)
# 		stall_set.append(sale.product.product.stall)
# 	if curr_balance < total:
# 		value = total - curr_balance
# 		try:
# 			bitsian = Bitsian.objects.get(email=request.user.email)
# 			bitsian = True
# 		except:
# 			bitsian = False
# 		return render(request, 'storewebapp/add_money.html', {'bitsian':bitsian, 'value':value})
# 	stall_set = set(stall_set)
# 	data = []
# 	stg_ids = []
# 	try:
# 		bitsian = Bitsian.objects.get(email=request.user.email)
# 		is_bitsian = True
# 	except:
# 		is_bitsian=False
# 		participant = Participant.objects.get(user=request.user)
# 	for stall in stall_set:
# 		transaction = Transaction.objects.create(wallet=wallet, t_type="buy")
# 		if is_bitsian:
# 			stall_group = StallGroup.objects.create(transaction=transaction, is_bitsian=is_bitsian,stall=stall, user=user, bitsian=bitsian)
# 		else:
# 			stall_group = StallGroup.objects.create(transaction=transaction, is_bitsian=is_bitsian,stall=stall, user=user, participant=participant)
# 		data.append([stall, stall_group, transaction])
# 		stg_ids.append(stall_group.id)
# 	for sale in sales:
# 		quantity =sale.quantity
# 		product = sale.product
# 		if product.product.p_type.name == 'Apparel':
# 			product.quantity_left -= sale.quantity
# 			product.save()
# 		elif product.product.p_type.name == 'ProfShow':
# 			prof_show = product.product.prof_show
# 			s = get_attendance_count(prof_show)
# 			if is_bitsian:
# 				try:
# 					attendance = Attendance.objects.get(bitsian=bitsian, prof_show=prof_show)
# 					attendance.count += int(sale.quantity)
# 					attendance.save()
# 				except:
# 					attendance = Attendance()
# 					attendance.bitsian = bitsian
# 					attendance.prof_show = prof_show
# 					attendance.paid = True
# 					attendance.count = int(quantity)
# 					attendance.save()
# 			else:
# 				try:
# 					attendance = Attendance.objects.get(participant=participant, prof_show=prof_show)
# 					attendance.count += int(sale.quantity)
# 					attendance.save()
# 				except:
# 					attendance = Attendance()
# 					attendance.participant = participant
# 					attendance.prof_show = prof_show
# 					attendance.paid = True
# 					attendance.count = int(quantity)
# 					attendance.save()
# 			s = Attendance.objects.all().count()
# 			attendance.number = s
# 			attendance.save()

# 		stall = product.product.stall
# 		stall_group = StallGroup.objects.filter(id__in=stg_ids).get(stall=stall)
# 		transaction = stall_group.transaction
# 		stall_group.amount += product.price * quantity
# 		cart.amount -= product.price * quantity
# 		cart.save()
# 		stall_group.unique_code = str(random.randint(1000, 9999))
# 		stall_group.orderid = str(stall_group.id) + stall.name[:3] + wallet.userid
# 		stall_group.save()
# 		transaction.value += product.price * quantity
# 		transaction.save()
# 		sale.stall_group = stall_group
# 		sale.paid=True
# 		sale.save()
# 		cart.sales.remove(sale)
	
# 	##for vendor
# 	for stg_id in stg_ids:
# 		stg = StallGroup.objects.get(id=stg_id)
# 		if stg.stall.id == 12:
# 			stg.code_requested=True
# 			stg.order_ready=True
# 			stg.order_complete=True
# 			stg.save()
# 		t = stg.transaction
# 		db.child('stall').child(stg.stall.id).child(stg.id).set(StallGroupSerializer(stg).data)
# 		db.child('wallet').child(wallet.uid).child('transactions').child(t.id).set(TransactionSerializer(t).data)
# 	##for the user
# 	wallet.curr_balance -= total
# 	wallet.save()
# 	db.child('wallet').child(wallet.uid).child('wallet').set(WalletSerializer(wallet).data)
# 	context = {'error_heading' : "Order Successful",
#                 'message' :  'Your order has been placed. Sit back and relax.',
#                 'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 	return render(request, 'storewebapp/message.html', context)

# @login_required
# def generate_code(request, sg_id):
# 	stall_group = StallGroup.objects.get(id=sg_id)
# 	if not stall_group.user == request.user:
# 	    context = {'error_heading' : "Invalid access",
# 	                'message' :  'Cannot access this page.',
# 	                'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 	    return render(request, 'storewebapp/message.html', context)
# 	if stall_group.cancelled:
# 		context = {'error_heading' : "Invalid access",
# 	                'message' :  'Cannot access this page.',
# 	                'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 		return render(request, 'storewebapp/message.html', context)
# 	if not stall_group.order_ready:
# 		context = {'error_heading' : "Order Not  Ready",
# 	                'message' :  'Cannot access this page.',
# 	                'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 		return render(request, 'storewebapp/message.html', context)
# 	stall_group.code_requested = True
# 	stall_group.save()
# 	# transaction = stall_group.transaction
# 	stall = stall_group.stall
# 	# wallet = transaction.wallet
# 	# db.child('stall').child(stall.id).child(stall_group.id).set(StallGroupSerializer(stall_group).data)
# 	# db.child('wallet').child(wallet.uid).child('transactions').child(transaction.id).set(TransactionSerializer(transaction).data)
# 	context = {'error_heading' : str(stall_group.unique_code), 'message' :  'Unique code.', 'url':request.build_absolute_uri(reverse('storewebapp:home'))}
# 	return render(request, 'storewebapp/message.html', context)

# def user_logout(request):
#     logout(request)
#     return redirect('storewebapp:home')

# def get_attendance_count(prof_show):
# 	sum_ = 1
# 	for i in Attendance.objects.filter(prof_show=prof_show):
# 		sum_ += (i.count+i.passed_count)
# 	return sum_

# def generate_qr(request):
#     text = request.GET.get('text')
#     qr = generate_qr_code(text)
#     response = HttpResponse(content_type="image/jpeg")
#     qr.save(response, "JPEG")
#     return response

# def generate_qr_code(data):
# 	import qrcode
# 	import qrcode.image.svg
# 	from PIL import Image
# 	part_code = qrcode.make(data)
# 	# part_code = 
# 	return part_code


# def send_mail_think_again():

# 	body = """<p>Greetings!</p>

# <p>&nbsp;</p>

# <p>The Think Again Conclave presents its Second&nbsp;Speaker, Ms.&nbsp;Sheila Dikshit.&nbsp;</p>

# <p>&nbsp;</p>

# <p>Be a witness to the inspiring story of the longest serving chief minister of Delhi, and one of the most influential politicians of our country, Sheila Dikshit, at the Think Again Conclave in her Online Talk in APOGEE 2018. Having served as a Union Minister during 1986-1989, her policies were influential in shaping the current Indian framework for Parliamentary affairs. The Dara Shikoh award that was conferred on her rightly justifies her contribution in upholding and nurturing the values of peace.</p>

# <p>&nbsp;</p>

# <p>Date:&nbsp;24th February 2018&nbsp;</p>

# <p>Venue: NAB Auditorium</p>

# <p>Time:&nbsp;2:30 PM</p>

# <p>Topic of Talk: &lsquo;Citizen Delhi&rsquo;</p>

# <p>&nbsp;</p>

# <p>Be there!</p>

# <p>&nbsp;</p>

# <p>Contact:&nbsp;</p>

# <p>Awais -<a href="tel:9611947866" target="_blank">9611947866</a></p>

# <p>&nbsp;</p>

# <p>Regards</p>

# <p>&nbsp;</p>

# <p>Department of Paper Evaluation &amp; Presentation</p>"""
# 	content = Content('text/html', body)
# 	subject = "Think Again Conclave | Sheila Dikshit"
# 	from_email = Email('webmaster@bits-apogee.org')
# 	for b in Bitsian.objects.all():
# 		to_email = Email(b.email)
# 		mail = Mail(from_email, subject, to_email, content)
# 		sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
# 		try:
# 			response = sg.client.mail.send.post(request_body=mail.get())
# 			print('mail sent to  ' + b.email)
# 		except Exception as e:
# 			print('Error with  ' + b.email)
# 	for b in Participant.objects.filter(firewallz_passed=True):
# 		to_email = Email(b.email)
# 		mail = Mail(from_email, subject, to_email, content)
# 		sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
# 		try:
# 			response = sg.client.mail.send.post(request_body=mail.get())
# 			print('mail sent to  ' + b.email)
# 		except Exception as e:
# 			print('Error with  ' + b.email)


# def send_mail_think_again():

# 	body = """<p>Greetings!</p>

# <p>&nbsp;</p>

# <p><strong>Think Again Conclave Speaker #3</strong></p>

# <p>&nbsp;</p>

# <p><strong>Rajdeep Sardesai</strong></p>

# <p>&nbsp;</p>

# <p>Resilient, alert and distinguished, this Think Again speaker has been a journalist since 1988. In a career spanning 30 years, Mr. Rajdeep Sardesai, as a journalist and the editor in chief of one of the biggest news-houses of India, he has always asked the hard-hitting questions that many refuse to ask. Listen to his galvanizing words in his Online Talk during APOGEE 2018.</p>

# <p>&nbsp;</p>

# <p>Date:&nbsp;25th February 2018</p>

# <p>Venue: NAB Audi</p>

# <p>Time:&nbsp;2:00 PM</p>

# <p>&nbsp;</p>

# <p>Be there!</p>

# <p>&nbsp;</p>

# <p>Contact:&nbsp;</p>

# <p>Awais -<a href="tel:9611947866" target="_blank">9611947866</a></p>

# <p>&nbsp;</p>

# <p>Regards</p>

# <p>&nbsp;</p>

# <p>Department of Paper Evaluation &amp; Presentation&nbsp;</p>
# """
# 	content = Content('text/html', body)
# 	subject = "Papyrus Trails | Women’s Panel"
# 	from_email = Email('webmaster@bits-apogee.org')
# 	for b in Bitsian.objects.all():
# 		to_email = Email(b.email)
# 		mail = Mail(from_email, subject, to_email, content)
# 		sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
# 		try:
# 			response = sg.client.mail.send.post(request_body=mail.get())
# 			print('mail sent to  ' + b.email)
# 		except Exception as e:
# 			print('Error with  ' + b.email)
# 	for b in Participant.objects.filter(firewallz_passed=True):
# 		to_email = Email(b.email)
# 		mail = Mail(from_email, subject, to_email, content)
# 		sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
# 		try:
# 			response = sg.client.mail.send.post(request_body=mail.get())
# 			print('mail sent to  ' + b.email)
# 		except Exception as e:
# 			print('Error with  ' + b.email)




# def send_mail_bsf():
# 	import os
# 	import base64
# 	body = """<p>This APOGEE,&nbsp;entry&nbsp;to the Auditorium during the&nbsp;Prof-show&nbsp;<strong>N2O</strong>&nbsp;is as follows:<br />
# <strong>For faculty, sponsors and on spot signings&ndash;&nbsp;Main Gate of Auditorium</strong><br />
# 1)&nbsp;<strong>All Girls irrespective of their QR Code no&rsquo;s should enter only from&nbsp;</strong>Lower (ground floor) corridor connecting FD-3 building and Auditorium.<br />
# 2)&nbsp;For boys having ID&nbsp;from<strong>&nbsp;1 to 500</strong>&nbsp;entry&nbsp;is from&nbsp;<strong>lower corridor</strong>&nbsp;connecting&nbsp;<strong>FD-2</strong>&nbsp;building and Auditorium.<br />
# 3)For boys having ID from&nbsp;<strong>501&nbsp;</strong>to&nbsp;<strong>1000</strong>&nbsp;entry is from&nbsp;<strong>upper corridor&nbsp;</strong>connecting&nbsp;<strong>FD-2</strong>&nbsp;building and Auditorium.<br />
# 4)For boys having ID from&nbsp;<strong>1001&nbsp;</strong>and&nbsp;<strong>above</strong>&nbsp;entry is from&nbsp;<strong>upper corridor&nbsp;</strong>connecting&nbsp;<strong>FD-3</strong>&nbsp;building and Auditorium.<br />
# 5)&nbsp;<strong>Bags and Eatables</strong>&nbsp;are&nbsp;<strong>not allowed.</strong><br />
# It is mandatory to carry&nbsp;<strong>BITSIAN ID</strong>&nbsp;cards along with your QR code when you enter the auditorium.<br />
# No one will be allowed inside without ID card at any cost.<br />
# We request all of you to co-operate with us for a successful APOGEE-2018<br />
# Bringing any&nbsp;<strong>intoxicating</strong>&nbsp;substance is strictly prohibited.</p>

# <p><strong>Strict action</strong>&nbsp;will be taken by the institute against people found guilty of substance abuse.</p>

# <p>&nbsp;Kindly find the attached herewith a screenshot of the app after you are successfully signed up for the event.<br />
# Where to find your QR code?<br />
# 1. Android version&nbsp; :<br />
# - download the app from this link:&nbsp;<a href="http://www.bits-apogee.org/app" target="_blank">www.bits-apogee.org/app</a><br />
# - click on profile icon in the bottom left corner<br />
# -&nbsp;login through BITS mail<br />
# - now you can view your QR code and ID.<br />
# 2. Web Application :&nbsp;&nbsp;<br />
# - open the app at his link:&nbsp;<a href="http://www.bits-apogee.org/wallet" target="_blank">www.bits-apogee.org/wallet</a><br />
# - Click on Sign In using BITSMail and log in using BITS email id.<br />
# - To see QR Code, click on Show QR Code.<br />
# - You can also view your ID below the QR Code.</p>

# <p>&nbsp;</p>

# <p><br />
# For further queries,<br />
# Contact:<br />
# Sai Appala Raju Indukuri&nbsp;<a href="tel:8209182646" target="_blank">(8209182646</a>)<br />
# Krishna Chaitanya<a href="tel:8639832585" target="_blank">(8639832585</a>)<br />
# Jayant&nbsp;<a href="tel:7689067883" target="_blank">(7689067883</a>)<br />
# Department of Audi Force</p>"""

# 	content = Content('text/html', body)
# 	subject = "N2O Entry Plan"
# 	from_email = Email('controls@bits-apogee.org')
# 	lists = ['4.jpg', '5.jpg']
# 	names = lists
# 	encoded = []
# 	attachments = []
# 	for i,c in enumerate(lists):
# 		with open(os.path.join(BASE_DIR, 'media', 'bsf', c), "rb") as img:
# 			encoded.append(base64.b64encode(img.read()))
# 			a=Attachment()
# 			a.content=encoded[i]
# 			a.filename=names[i]
# 			attachments.append(a)
# 	for b in ['f2016023@pilani.bits-pilani.ac.in']:
# 		to_email = Email(b)
# 		sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
# 		mail = Mail(from_email, subject, to_email, content)
# 		for j in attachments:
# 			mail.add_attachment(j)
# 		try:
# 			response = sg.client.mail.send.post(request_body=mail.get())
# 			print('mail sent to  ' + b)
# 		except Exception as e:
# 			print('Error with  ' + b)


# 	for a in Attendance.objects.filter(prof_show__id=3):
# 		try:
# 			b = a.bitsian
# 			email = b.email
# 		except:
# 			b = a.participant
# 			email = b.email
# 	# for b in Bitsian.objects.all():
# 		to_email = Email(b.email)
# 		sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
# 		mail = Mail(from_email, subject, to_email, content)
# 		for j in attachments:
# 			mail.add_attachment(j)
# 		try:
# 			response = sg.client.mail.send.post(request_body=mail.get())
# 			print('mail sent to  ' + b.email)
# 		except Exception as e:
# 			print('Error with  ' + b.email)



# 	# for b in Participant.objects.filter(firewallz_passed=True):
# 	# 	to_email = Email(b.email)
# 	# 	sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
# 	# 	mail = Mail(from_email, subject, to_email, content)
# 	# 	for j in attachments:
# 	# 		mail.add_attachment(j)
# 	# 	try:
# 	# 		response = sg.client.mail.send.post(request_body=mail.get())
# 	# 		print('mail sent to  ' + b.email)
# 	# 	except Exception as e:
# 	# 		print('Error with  ' + b.email)












# def send_mail_bsf1():
# 	import os
# 	import base64
# 	body = """<p>Greetings!</p>

# <p>&nbsp;</p>

# <p><strong>Papyrus Trails: A Journalist Panel on Fake News and Ethics in Journalism</strong></p>

# <p>&nbsp;</p>

# <p>We bring to you, in association with HPC, a panel on Free Speech, Fake News and Ethics in Journalism - &#39;The Offenders&#39; Game&#39; featuring&nbsp;<strong>Ashutosh</strong>, the spokesman for AAP and a former Managing Director of IBN7 and&nbsp;<strong>Paranjoy Guhha Thakurta</strong>&nbsp;a renowned journalist, political commentator, author and a documentary film maker. Watch some of the most distinguished journalists of our country discuss the raging problems in today&#39;s media. Come be a part of the discussion on journalistic ethics and their relevance in modern society.</p>

# <p>&nbsp;</p>

# <p>Date:&nbsp;25th February 2018</p>

# <p>Venue: NAB Audi</p>

# <p>Time:&nbsp;4:30 PM</p>

# <p>&nbsp;</p>

# <p>Be there!</p>

# <p>&nbsp;</p>

# <p>Contact:&nbsp;</p>

# <p>Awais -<a href="tel:9611947866" target="_blank">9611947866</a></p>

# <p>&nbsp;</p>

# <p>Regards</p>

# <p>&nbsp;</p>

# <p>Department of Paper Evaluation &amp; Presentation</p>

# """

# 	content = Content('text/html', body)
# 	subject = "Papyrus Trails | Journalist Panel"
# 	from_email = Email('webmaster@bits-apogee.org')
# 	lists = ['unnamed1.jpg']
# 	names = lists
# 	encoded = []
# 	attachments = []
# 	for i,c in enumerate(lists):
# 		with open(os.path.join(BASE_DIR, 'media', 'bsf', c), "rb") as img:
# 			encoded.append(base64.b64encode(img.read()))
# 			a=Attachment()
# 			a.content=encoded[i]
# 			a.filename=names[i]
# 			attachments.append(a)
# 	# for b in ['f2016023@pilani.bits-pilani.ac.in']:
# 	# 	to_email = Email(b)
# 	# 	sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
# 	# 	mail = Mail(from_email, subject, to_email, content)
# 	# 	for j in attachments:
# 	# 		mail.add_attachment(j)
# 	# 	try:
# 	# 		response = sg.client.mail.send.post(request_body=mail.get())
# 	# 		print('mail sent to  ' + b)
# 	# 	except Exception as e:
# 	# 		print('Error with  ' + b)


# 	for b in Bitsian.objects.all():
# 		to_email = Email(b.email)
# 		sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
# 		mail = Mail(from_email, subject, to_email, content)
# 		for j in attachments:
# 			mail.add_attachment(j)
# 		try:
# 			response = sg.client.mail.send.post(request_body=mail.get())
# 			print('mail sent to  ' + b.email)
# 		except Exception as e:
# 			print('Error with  ' + b.email)
# 	for b in Participant.objects.filter(firewallz_passed=True):
# 		to_email = Email(b.email)
# 		sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
# 		mail = Mail(from_email, subject, to_email, content)
# 		for j in attachments:
# 			mail.add_attachment(j)
# 		try:
# 			response = sg.client.mail.send.post(request_body=mail.get())
# 			print('mail sent to  ' + b.email)
# 		except Exception as e:
# 			print('Error with  ' + b.email)

def dummy_stalls(request):
	return JsonResponse({})
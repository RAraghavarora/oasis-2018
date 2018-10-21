from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render,redirect

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

class Login(APIView):

	renderer_classes = (TemplateHTMLRenderer,)
	parser_classes = (FormParser,JSONParser, MultiPartParser)

	def post(self, request):
		
		try:
			username = request.data['username']
			password = request.data['password']
		except KeyError as missing:
			msg = 'The following field was missing: {}'.format(missing)
			messages.warning(request, msg)
			return redirect(request.META.get('HTTP_REFERER'))

		user = authenticate(username=username, password=password)

		if user is None:
			messages.warning(request, 'Invalid credentials')
			return redirect(request.META.get('HTTP_REFERER'))

		login(request, user)

		return redirect('ems:index')

	def get(self, request):

		return Response(template_name='ems/login.html')


class Logout(APIView):

	renderer_classes = (TemplateHTMLRenderer,)

	def post(self, request):

		logout(request)
		return redirect('ems:login')

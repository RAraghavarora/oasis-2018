from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

class Login(APIView):

	#renderer_classes = (TemplateHTMLRenderer,)

	def post(self, request):

		try:
			username = request.POST['username']
			password = request.POST['password']
		except KeyError as missing:
			msg = 'The following field was missing: {}'.format(missing)
			messages.warning(request, msg)
		return redirect()

		user = authenticate(username=username, password=password)

		if user is None:
			messages.warning(request, 'Invalid credentials')
			return redirect(request.META.get('HTTP_REFERER'))

		login(request, user)
		return redirect('ems:index')


class Logout(APIView):

	def post(self, request):

		logout(request)
		return redirect('ems:index')

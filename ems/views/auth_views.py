from rest_framework.views import APIView
from django.contrib.auth import authenticate

class Login(APIView):

	def post(self, request):
		username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('ems:index')
		else:
			messages.warning(request, 'Invalid credentials')
			return redirect(request.META.get('HTTP_REFERER'))
		
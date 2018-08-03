#---Imports---#
#Django Imports
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
#Self Imports
from . import views
#---End of Imports---#

app_name = 'registrations'

urlpatterns = [
				url(r'^api-token-auth/', obtain_jwt_token),
				url(r'^intro/$', views.PreRegistration, name="PreRegistration"),
			]
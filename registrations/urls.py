#---Imports---#
#Django Imports
from django.conf.urls import url
#Self Imports
from . import views
#---End of Imports---#

app_name = 'registrations'

urlpatterns = [
				url(r'^intro/$', views.PreRegistration, name="PreRegistration"),
			]
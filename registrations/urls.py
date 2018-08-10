from django.conf.urls import url

from registrations import views

app_name = 'registrations'

urlpatterns = [				
				url(r'^intro/$', views.PreRegistration, name="PreRegistration"),
			]

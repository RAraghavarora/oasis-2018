from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token

from registrations import views

app_name = 'registrations'

urlpatterns = [
				url(r'^api-token-auth/', obtain_jwt_token),
				url(r'^intro/$', views.PreRegistration, name="PreRegistration"),
			]

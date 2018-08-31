from django.conf.urls import url

from registrations.views import intro,participants

app_name = 'registrations'

urlpatterns = [
				url(r'^intro/$', intro.PreRegistration.as_view(), name="PreRegistration"),
				url(r'^$',participants.index,name='home'),
				url(r'^hello',participants.abc,name='index')
			]

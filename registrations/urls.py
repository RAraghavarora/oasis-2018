from django.conf.urls import url

from registrations.views import intro,participants,cr

app_name = 'registrations'

urlpatterns = [
				url(r'^intro/$', intro.PreRegistration.as_view(), name="PreRegistration"),
				url(r'^$',participants.index,name='index'),
				url(r'^hello',participants.abc,name='home'),
				url(r'^email_confirm/(?P<token>\w+)',participants.email_confirm,name = 'email_confirm'),
				url(r'cr_approve',cr.approve,name='cr_approve')
			]

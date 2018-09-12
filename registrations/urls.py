from django.conf.urls import url

from registrations.views import intro,participants,cr
from django.contrib.auth.views import logout 

app_name = 'registrations'

urlpatterns = [
				url(r'^intro/$', intro.PreRegistration.as_view(), name="PreRegistration"),
				url(r'^$',participants.index,name='index'),
				url(r'^login',participants.home,name='home'),
				url(r'^email_confirm/(?P<token>\w+)',participants.email_confirm,name = 'email_confirm'),
				url(r'cr_approve',cr.approve,name='cr_approve'),
				url(r'^details/(?P<p_id>\d+)',cr.participant_details,name='participant_details'),
				url(r'^manage_events$',participants.manage_events,name='manage_events'),
				url(r'^participant_profile_card',participants.get_profile_card,name='participant_profilecard'),
				url(r'^logout$',logout,name='logout'),
				# url(r'^cr_profile_card',cr.get_profile_card,name='cr_profilecard'),
				# url(r'^payment$',participants.payment,name='make_payment'),
				# url(r'^hello$',participants.payment_response,name='hello')
			]

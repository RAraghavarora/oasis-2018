from django.conf.urls import url
from . import  views

app_name='regsoft'

urlpatterns=[
    
   #url(r'^$', views.index, name='index'),
   ###FIREWALLS###
    url(r'^firewallz/$',views.firewallz_home,name = 'firewallz_home'),
    url(r'^firewallz/(?P<c_id>\d+)/$', views.firewallz_approval, name='firewallz_approval'),
    url(r'^firewallz/groups/(?P<g_id>\d+)/$', views.get_group_list, name='get_group_list'),
	url(r'^firewallz/add_guest/$', views.add_guest, name='add_guest'),
	url(r'^firewallz/remove_guests/$', views.remove_guests, name='remove_guests'),
	url(r'^firewallz/add_participant/$', views.add_participant, name='add_participant'),
	url(r'^firewallz/delete_group/(?P<g_id>\d+)/$', views.delete_group, name='delete_group'),

    ###Recnacc###
 #    url(r'^recnacc/$', views.recnacc_home, name='recnacc_home'),
	# url(r'^recnacc/allocate/(?P<g_id>\d+)/$', views.allocate_participants, name='allocate_participants'),
	# url(r'^recnacc/grouplist/(?P<c_id>\d+)/$', views.recnacc_group_list, name='recnacc_group_list'),
	# url(r'^recnacc/group_vs_bhavan/$', views.group_vs_bhavan, name='group_vs_bhavan'),
	# url(r'^recnacc/bhavans/$', views.recnacc_bhavans, name='recnacc_bhavans'),
	# url(r'^recnacc/room_details/$', views.room_details, name='room_details'),
	# url(r'^recnacc/bhavan_details/(?P<b_id>\d+)/$', views.bhavan_details, name='bhavan_details'),
	# url(r'^recnacc/manage_vacancies/(?P<r_id>\d+)/$', views.manage_vacancies, name='manage_vacancies'),
    # url(r'^recnacc/colleges/$', views.recnacc_college_details, name='recnacc_college_details'),
    # url(r'^recnacc/college_detail/(?P<c_id>\d+)/$', views.college_detail, name='college_detail'),
	# url(r'^recnacc/checkout/$', views.checkout_college, name="checkout_college"),
	# url(r'^recnacc/checkout/(?P<c_id>\d+)/$', views.checkout, name="checkout"),
	# url(r'^recnacc/checkout/groups/(?P<c_id>\d+)/$', views.checkout_groups, name="checkout_groups"),
	# url(r'^recnacc/checkout/groupdetails/(?P<ck_id>\d+)/$', views.ck_group_details, name="ck_group_details"),
	# url(r'^recnacc/checkout/master_checkout/$', views.master_checkout, name="master_checkout"),

	### CONTROLS ###
	url(r'^controls',views.controls_home)
]
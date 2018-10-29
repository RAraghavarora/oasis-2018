from django.conf.urls import url
from . import  views

app_name='regsoft'

urlpatterns=[

   url(r'^$', views.index, name='index'),
   ###FIREWALLS###
    url(r'^firewallz/?$',views.firewallz_home,name = 'firewallz_home'),
    url(r'^firewallz/(?P<c_id>\d+)/?$', views.firewallz_approval, name='firewallz_approval'),
    url(r'^firewallz/groups/(?P<g_id>\d+)/?$', views.get_group_list, name='get_group_list'),
	url(r'^firewallz/add_guest/?$', views.add_guest, name='add_guest'),
	url(r'^firewallz/remove_guests/?$', views.remove_guests, name='remove_guests'),
	url(r'^firewallz/add_participant/?$', views.add_participant, name='add_participant'),
	url(r'^firewallz/delete_group/(?P<g_id>\d+)/?$', views.delete_group, name='delete_group'),
	url(r'^firewallz/approved_groups/?$', views.approved_groups, name='approved_groups'),


    ###Recnacc###
    url(r'^recnacc/?$', views.recnacc_home, name='recnacc_home'),
	url(r'^recnacc/allocate/(?P<g_id>\d+)/?$', views.allocate_participants, name='allocate_participants'),
	url(r'^recnacc/grouplist/(?P<c_id>\d+)/?$', views.recnacc_group_list, name='recnacc_group_list'),
	url(r'^recnacc/group_vs_bhavan/?$', views.group_vs_bhavan, name='group_vs_bhavan'),
	url(r'^recnacc/bhavans/?$', views.recnacc_bhavans, name='recnacc_bhavans'),
	url(r'^recnacc/room_details/?$', views.room_details, name='room_details'),
	url(r'^recnacc/bhavan_details/(?P<b_id>\d+)/?$', views.bhavan_details, name='bhavan_details'),
	url(r'^recnacc/manage_vacancies/(?P<r_id>\d+)/?$', views.manage_vacancies, name='manage_vacancies'),
    url(r'^recnacc/colleges/?$', views.recnacc_college_details, name='recnacc_college_details'),
	url(r'^recnacc/checkout/?$', views.checkout_college, name="checkout_college"),
	url(r'^recnacc/checkout/(?P<c_id>\d+)/?$', views.checkout, name="checkout"),
	url(r'^recnacc/checkout/groups/(?P<c_id>\d+)/?$', views.checkout_groups, name="checkout_groups"),
	url(r'^recnacc/checkout/groupdetails/(?P<ck_id>\d+)/?$', views.ck_group_details, name="ck_group_details"),
	url(r'^recnacc/checkout/master_checkout/?$', views.master_checkout, name="master_checkout"),

	### CONTROLZ ###
	url(r'^controlz/?$', views.controlz_home, name='controlz_home'),
	url(r'^controlz/createbill/(?P<g_id>\d+)/?$', views.create_bill, name='create_bill'),
    url(r'^controlz/bills/?$', views.show_all_bills, name='show_all_bills'),
	url(r'^controlz/firewallz/profile_cards/?$', views.get_profile_card, name='get_profile_card'),
	url(r'^controlz/recnacc_list/?$', views.recnacc_list, name='recnacc_list'),
	url(r'^controlz/recnacc_list/(?P<g_id>\d+)/?$', views.recnacc_list_group, name='recnacc_list_group'),
	url(r'^controlz/generate_recnacc_list/?$', views.generate_recnacc_list, name='generate_recnacc_list'),
	url(r'^controlz/show_all_bills/?$', views.show_all_bills, name='show_all_bills'),
	url(r'^controlz/show_college_bills/(?P<c_id>\d+)/?$', views.show_college_bills, name='show_college_bills'),
	url(r'^controlz/bill_details/(?P<b_id>\d+)/?$', views.bill_details, name='bill_details'),
	url(r'^controlz/delete_bill/(?P<b_id>\d+)/?$', views.delete_bill, name='delete_bill'),
	url(r'^controlz/print_bill/(?P<b_id>\d+)/?$', views.print_bill, name='print_bill'),
	url(r'^firewallz/profile_card_group/(?P<g_id>\d+)/?$',views.get_profile_card_group, name = 'get_profile_card_group'),

	url(r'^logout$',views.user_logout, name = 'logout'),

	### INVENTORY ###
	url(r'inventory/?$', views.dashboard, name='dashboard'),
	url(r'inventory/tenderform/?$', views.tender_new_form, name='tender_form'),
	url(r'inventory/dc_login/?$', views.dc_login, name='dc_login'),
	url(r'inventory/dc_new_entry/(?P<dc_id>\d+)/?$', views.dc_new_entry, name='dc_new_entry'),
	url(r'inventory/dc_remove_entry/(?P<dc_id>\d+)/?$', views.dc_remove_entry, name='dc_remove_entry'),
	url(r'inventory/dc_view_status/(?P<dc_id>\d+)/?$', views.dc_view_status, name='dc_view_status'),

	url(r'inventory/tender_home/?$', views.tender_home, name='tender_home'),
	url(r'inventory/tender_new_form/?$', views.tender_new_entry, name='tender_new_entry'),
	url(r'inventory/tender_return/$',views.tender_remove_home, name='tender_remove_home'),
	url(r'inventory/tender_in/$',views.tender_in, name='tender_in'),
	url(r'inventory/tender_remove_form/(?P<l_id>\d+)/?$', views.tender_remove_entry, name='tender_remove_entry'),
	url(r'inventory/tender_view_status/?$', views.tender_view_status, name='tender_view_status'),

	url(r'inventory/mattress_home/?$', views.mattress_home, name='mattress_home'),
	url(r'inventory/mattress_new_entry/?$', views.mattress_new_entry, name='mattress_new_entry'),
	url(r'inventory/mattress_return_home/?$', views.mattress_return_home, name='mattress_return_home'),
	url(r'inventory/mattress_in/?$', views.mattress_in, name='mattress_in'),
	url(r'inventory/mattress_remove_entry/(?P<l_id>\d+)/?$', views.mattress_remove_entry, name='mattress_remove_entry'),
	url(r'inventory/mattress_view_status/?$', views.mattress_view_status, name='mattress_view_status'),

	url(r'inventory/excel/?$', views.excel, name='excel'),
	url(r'excel/',views.excel2,name='hads'),
	url(r'indo_excel/',views.indo_excel,name='indo_data'),
	url(r'shankar_excel/',views.shankar_excel,name='shankar_data')





]
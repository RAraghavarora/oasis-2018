from django.conf.urls import url
from . import views

app_name = 'storewebapp'

urlpatterns = [
	url(r'^$', views.home, name='home'),
    url(r'^bitsian_login/$', views.bitsian_login, name='bitsian_login'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^stalls/(?P<stall_id>\d+)/$', views.stalls, name="stalls"),
    url(r'^stalls/$', views.dummy_stalls, name="stalls"),
    url(r'^view_cart/$', views.view_cart, name='view_cart'),
	# url(r'^participant_login/$', views.participant_login, name='participant_login'),
    # url(r'^get_products/(?P<stall_id>\d+)/$', views.get_products, name='get_products'),
    # url(r'^add_to_cart/(?P<stall_id>\d+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^add_money/$', views.add_money, name='add_money'),
    url(r'^send_money/$', views.send_money, name='send_money'),
    # url(r'^transfer_money/$', views.transfer_money, name='transfer_money'),
    # url(r'^view_cart/$', views.view_cart, name='view_cart'),
    # url(r'^user_logout/$', views.user_logout, name='user_logout'),
    # url(r'^add_money_request/$', views.add_money_request, name='add_money_request'),
    # url(r'^add_money_response/$', views.add_money_response, name='add_money_response'),
    url(r'^prof_show_details/$', views.prof_show_details, name='prof_show_details'),
    url(r'^show_transactions/$', views.show_transactions, name='show_transactions'),
    # url(r'^transaction_details/(?P<t_id>\d+)/$', views.transaction_details, name='transaction_details'),
    # url(r'^get_sg_products/(?P<sg_id>\d+)/$', views.get_sg_products, name='get_sg_products'),
    # url(r'^generate_code/(?P<sg_id>\d+)/$', views.generate_code, name='generate_code'),
    # url(r'^checkout/?$', views.checkout_payment, name="checkout"),
    # url(r'^generate_qr/?$', views.generate_qr, name="generate_qr"),
    url(r'qr/(?P<data>.+)/$',views.generate_qr,name='qr')
]

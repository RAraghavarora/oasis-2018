from django.conf.urls import url

from shop.views import auth_views
from shop.views import ewallet_views
from shop.views import orders_views
from shop.views import stalls_views
from shop.views import misc_views

app_name="shop"

urlpatterns = [
    url('transfer', ewallet_views.Transfer.as_view(), name="transfer"),
    url('place-order', orders_views.PlaceOrder.as_view(), name="place-order"),

    url(r'^auth/', auth_views.Authentication.as_view(), name = "auth"),

    url(r'^stalls/$', stalls_views.StallsList.as_view(), name = 'stalls'),
    url(r'^stalls/(?P<stall_id>\d+)/$', stalls_views.ProductsList.as_view(), name = 'products'),

    url(r'^stalls/client/orders/$', stalls_views.StallOrdersList.as_view(), name = 'stall-orders'),
    url(r'^stalls/client/order-response/$', stalls_views.StallOrderStatus.as_view(), name = 'stall-order-status'),

    # url(r'^profile/$', misc_views.getProfile.as_view(), name="get-profile"),
]

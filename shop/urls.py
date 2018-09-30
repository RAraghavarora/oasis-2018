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
    url(r'^addmoney$', ewallet_views.AddMoney.as_view(), name="AddMoney" ),
    url(r'^addmoneyresponse', ewallet_views.AddMoneyResponse.as_view(), name="AddMoneyResponse"),

    url(r'^auth/', auth_views.Authentication.as_view(), name = "auth"),

    url(r'^stalls/$', stalls_views.StallsList.as_view(), name = 'stalls'),
    url(r'^stalls/(?P<stall_id>\d+)/$', stalls_views.ProductsList.as_view(), name = 'products'),

    url(r'^stalls/client/orders/$', stalls_views.StallOrdersList.as_view(), name = 'stall-orders'),
    url(r'^stalls/client/order-response/$', stalls_views.StallOrderStatus.as_view(), name = 'stall-order-status'),

    # NOTE: these endpoints, despite being "GET" endpoints, require a POST request.
    url(r'^get-profile/$', misc_views.GetProfile.as_view(), name='get-profile'),
    url(r'^get-orders/$', orders_views.GetOrders.as_view(), name='get-orders'),
    url(r'^get-tickets/$', orders_views.GetTickets.as_view(), name='get-tickets'),

    url(r'^consume-tickets/$', orders_views.ConsumeTickets.as_view(), name='consume-tickets'),
    url(r'^get-profshows/$', misc_views.GetProfShows.as_view(), name="get-profshows"),

]

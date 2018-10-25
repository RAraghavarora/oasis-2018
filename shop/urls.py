from django.conf.urls import url

from shop.views import auth_views
from shop.views import ewallet_views
from shop.views import orders_views
from shop.views import stalls_views
from shop.views import misc_views

app_name="shop"

urlpatterns = [
    url(r'transfer/', ewallet_views.Transfer.as_view(), name="transfer"),
    url(r'^add-money/$', ewallet_views.AddMoney.as_view(), name="AddMoney" ),
    url(r'^add-moneyresponse-ios/', ewallet_views.AddMoneyResponseIOS.as_view(), name="AddMoneyResponseIOS"),
    url(r'^add-moneyresponse-web/', ewallet_views.AddMoneyResponseWeb.as_view(), name="AddMoneyResponseWeb"),
    url(r'^add-moneyresponse-android/', ewallet_views.AddMoneyResponseAndroid.as_view(), name="AddMoneyResponseAndroid"),
    url(r'^ewallet/add-money/$', ewallet_views.AddByCash.as_view(), name="AddByCash"),

    url(r'^auth/$', auth_views.Authentication.as_view(), name = "auth"),
    url(r'^auth/ot/$', auth_views.OrganizationsAndTellersLogin.as_view(), name="auth-ot"),

    url(r'^stalls/$', stalls_views.StallsList.as_view(), name = 'stalls'),
    url(r'^stalls/(?P<stall_id>\d+)/$', stalls_views.ProductsList.as_view(), name = 'products'),
    url(r'^stalls/client/orders/$', stalls_views.StallOrdersList.as_view(), name = 'stall-orders'),
    url(r'^stalls/client/order-response/$', stalls_views.StallOrderStatus.as_view(), name = 'stall-order-status'),
    url(r'^stalls/client/switch/item/$', stalls_views.SwitchItemAvailability.as_view(), name = 'stall-switch-item'),
    url(r'^stalls/client/switch/$', stalls_views.SwitchStall.as_view(), name = 'stall-switch'),

    url(r'^orders/show-otp/$', orders_views.ShowOTP.as_view(), name = 'show-otp'),

    # NOTE: these endpoints, despite being "GET" endpoints, require a POST request. This is agreed to be a terrible thing but it was due to lack of time, and lots of pressure
    # will be improved upon in WalletX.
    url(r'place-order/', orders_views.PlaceOrder.as_view(), name="place-order"),
    url(r'^get-orders/$', orders_views.GetOrders.as_view(), name='get-orders'),
    url(r'^get-tickets/$', orders_views.GetTickets.as_view(), name='get-tickets'),
    url(r'^consume-tickets/$', orders_views.ConsumeTickets.as_view(), name='consume-tickets'),

    url(r'^get-profile/$', misc_views.GetProfile.as_view(), name='get-profile'),
    url(r'^get-profshows/$', misc_views.GetProfShows.as_view(), name="get-profshows"),

    url(r'^debug/info/$', misc_views.AppDebugInfo.as_view(), name="debug-info"),
]

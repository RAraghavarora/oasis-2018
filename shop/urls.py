from django.conf.urls import url

from shop.views import auth_views
from shop.views import ewallet_views
from shop.views import orders_views
#from shop.views import stalls_views
#from shop.views import test_views


app_name="shop"
urlpatterns = [
    url('transfer', ewallet_views.Transfer.as_view(), name="transfer"),
    url('place-order', orders_views.PlaceOrder, name="place-order"),

    url(r'^auth/', auth_views.Authentication.as_view(), name = "auth")
]

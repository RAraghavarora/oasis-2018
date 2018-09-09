from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

#from shop.views import auth_views
from shop.views import ewallet_views
from shop.views import orders_views
#from shop.views import stalls_views
#from shop.views import test_views


app_name="shop"
urlpatterns = [
    url('transfer', ewallet_views.Transfer.as_view(), name="transfer"),
    url('place-order', orders_views.PlaceOrder.as_view(), name="place-order"),

    #JWT Authentication
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token), #If JWT_ALLOW_REFRESH is True
    url(r'^api-token-verify/', verify_jwt_token),
]

from django.conf.urls import url, include
from shop.views import test_views

urlpatterns = [
    url(r'^test/', test_views.test, name = 'test'),
]
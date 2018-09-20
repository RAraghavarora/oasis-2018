from django.conf.urls import url

from . import views

app_name = "events"
urlpatterns = [
    url(r'^data/$', views.Data, name="data" ),
    url(r'^info/$', views.Info.as_view(), name="info" ),
]

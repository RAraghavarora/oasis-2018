from django.conf.urls import url

from . import views

app_name = "events"
urlpatterns = [
    url(r'^ied/$', views.IntroEventsData, name="ied" ),
]

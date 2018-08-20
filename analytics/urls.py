from django.conf.urls import url
from analytics import views

app_name="analytics"
urlpatterns = [
    url(r'views(?:/?)((?P<name>[\w\\+]+))?', views.views, name="views"),
    url(r'viewtime(?:/?)', views.viewTime, name="viewtime")
]

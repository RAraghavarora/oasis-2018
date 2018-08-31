from django.conf.urls import url
from pcradmin import views
app_name = 'pcradmin'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^college/$', views.college, name='college'),
    url(r'^college_rep/(?P<id>\d+)/$', views.select_college_rep, name='select_college_rep'),
    url(r'^approve_participations/(?P<id>\d+)/$', views.approve_participations, name='approve_participations'),

]

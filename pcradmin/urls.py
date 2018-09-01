from django.conf.urls import url
from pcradmin import views
app_name = 'pcradmin'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^college/$', views.college, name='college'),
    url(r'^college_rep/(?P<id>\d+)/$', views.select_college_rep, name='select_college_rep'),
    url(r'^approve_participations/(?P<id>\d+)/$', views.approve_participations, name='approve_participations'),
    url(r'^add_college/$', views.add_college, name='add_college'),    
    url(r'^logout/$', views.user_logout, name='user-logout'),
    url(r'^edit_particpant/(?P<part_id>\d+)/$', views.edit_participant, name='edit_participant'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^verify_profile/(?P<part_id>\d+)/$', views.edit_participant, name='verify_profile'),
    url(r'^stats/$', views.stats, name='stats'),
    url(r'^stats/(?P<order>\w+)/$', views.stats, name='stats'),
    url(r'^stats_event/(?P<e_id>\d+)/$', views.stats_event, name='stats_event'),
    url(r'^master_stats/$', views.master_stats, name='master_stats'),
    url(r'^final_confirmation/$', views.view_final, name='view_final'),

    #url(r'^final_confirmation/$', views.view_final, name='view_final'),
	

]

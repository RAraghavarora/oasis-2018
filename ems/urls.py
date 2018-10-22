from django.conf.urls import url

from ems.views import auth_views
from ems.views import clubdept_views
from ems.views import misc_views
from ems.views import team_views
from ems.views import event_views

app_name = 'ems'

urlpatterns = [
	url(r'^$', misc_views.Index.as_view(), name='index'),
	
	url(r'^login/$', auth_views.Login.as_view(), name="login"),
	url(r'^logout/$', auth_views.Logout.as_view(), name='logout'),

<<<<<<< HEAD
	url(r'^level_list/(?P<event_id>\d+)/$', event_views.LevelList.as_view(), name = "Level Detail"),

	url(r'^teams/list/(?P<event_id>\d+)/$', team_views.TeamList.as_view(), name = "team_home"),
	url(r'^teams/team_details/(?P<e_id>\d+)/(?P<team_id>\d+)/$', team_views.TeamDetail.as_view(), name="team_details"),
	url(r'^teams/add_or_delete/(?P<e_id>\d+)/$', team_views.TeamList.as_view(), name="add_team"),
=======
	# # url(r'^level_list/(?P<event_id>\d+)/$', event_views.LevelList.as_view(), name = "Level Detail"),

	# # url(r'^teams/list/(?P<event_id>\d+)/$', team_views.TeamList.as_view(), name = "team_home"),
	# # url(r'^teams/team_details/(?P<e_id>\d+)/(?P<team_id>\d+)/$', team_views.TeamDetail.as_view(), name="team_details"),
	# # url(r'^teams/add_or_delete/(?P<e_id>\d+)/$', team_views.TeamList.as_view(), name="add_team"),
>>>>>>> 7bc59735764a7a827fca10e2b6b5dd28e00dd794

	# url(r'^events/(?P<event_id>\d+)/levels/$', event_views.LevelList.as_view(), name = "event_levels"),
	# url(r'^events/levels/(?P<level_id>\d+)/$', event_views.LevelDetail.as_view(), name="show_level"),
	# url(r'^add_level/(?P<e_id>\d+)/$', event_views.LevelDetail.as_view(), name="add_level"),

	# url(r'^clubdept/$', clubdept_views.ClubDepartmentList, name="add_cd"),
	
	# url(r'^events_controls/$', misc_views.Index.as_view(), name="events_controls"),

]


#Events List

#Add team
#Update team
#Team details
#Teams List

#Add level
#Update Level
#Levels List

#Declare winner

#Add Judge
#Add ClubDepartment

#Controls Home

#Scores List
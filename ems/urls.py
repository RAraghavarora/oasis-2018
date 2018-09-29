from django.conf.urls import url

# from ems.views import auth_views
from ems.views import team_views
from ems.views import event_views

app_name = 'ems'

urlpatterns = [
				url(r'^level_list/(?P<event_id>\d+)/$', event_views.LevelList.as_view(), name="Level Detail"),
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
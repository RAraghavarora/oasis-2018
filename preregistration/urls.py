from django.conf.urls import url,include

from . import views


urlpatterns=[
    url(r'^poetryslam/$', views.PoetrySlamRegistration, name='PoetrySlamRegistration'),
    url(r'^rapwars/$', views.RapWarsRegistration, name='RapWarsRegistration'),
    url(r'^$',views.index,name='index'),    # for Rocktaves teams/bands registration
    url(r'^purpleprose/$',views.PurpleProseRegistration,name='PoetryProseRegistration'),
]
#urls to be reviewed

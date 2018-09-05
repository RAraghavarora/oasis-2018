"""oasis2018 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^preregistration/',include('preregistration.urls')),
    url(r'^events/',include('events.urls')),
    url(r'^registrations/',include('registrations.urls')),
    url(r'^analytics/', include('analytics.urls')),
    url(r'^pcradmin/',include('pcradmin.urls')),
]


urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, serve, document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL, serve, document_root=settings.MEDIA_ROOT)

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
<<<<<<< HEAD
    url(r'^shop/', include('shop.urls')),    
=======
    url(r'^shop/', include('shop.urls')),
>>>>>>> e2d0313ca55def15bc91fa4d040eabd6f07f6589
]


urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, serve, document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL, serve, document_root=settings.MEDIA_ROOT)

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from coolsite import settings
from profile.views import *
from django.urls import path, include

urlpatterns = [
    path('diodadmin/', admin.site.urls),
    path("", redir.as_view(), name="login_page"),
    path('profile/', include("profile.urls")),
    path('messenger/', include("messenger.urls")),
    path('api/', include("api.urls")),
    path('feed/', include("feed.urls")),
    path('search/', include("search.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from coolsite import settings
from profile.views import *
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", redir.as_view(), name="login_page"),
    path('profile/', include("profile.urls")),
    path('messenger/', include("messenger.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
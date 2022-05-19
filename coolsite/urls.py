from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import debug_toolbar
from coolsite import settings
from profile.views import *
from django.urls import path, include

urlpatterns = [
    path('diodadmin/', admin.site.urls),
    path("", redir.as_view(), name="login_page"),
    path("login/", login.as_view(), name="login_page"),
    path("signup/", signup.as_view(), name="signup_page"),
    path('profile/', include("profile.urls")),
    path('messenger/', include("messenger.urls")),
    path('api/', include("api.urls")),
    path('feed/', include("feed.urls")),
    path('search/', include("search.urls")),
    path('__debug__/', include(debug_toolbar.urls)),
]

handler404 = pagenotfound

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEPLOY:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.urls import path
from .views import *


urlpatterns = [
    path("", redir.as_view(), name="login_page"),
    path("<str:login>", profile.as_view(), name="profile_page"),
    path("submit_email/<str:login>", submit_email.as_view(), name="submit_email"),
]

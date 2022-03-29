from django.urls import path
from .views import *


urlpatterns = [
    path("", redir.as_view(), name="login_page"),
    path("login/", login.as_view(), name="login_page"),
    path("signup/", signup.as_view(), name="signup_page"),
    path("<str:login>", profile.as_view(), name="profile_page"),
    path("changedata/<str:login>", changedata.as_view(), name="changedata_page"),
]

handler404 = pagenotfound

from django.urls import path
from .views import *


urlpatterns = [
    path("<str:login>", chat.as_view(), name="chat"),
]

handler404 = pagenotfound
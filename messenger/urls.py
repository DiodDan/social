from django.urls import path
from .views import *


urlpatterns = [
    path("", chat.as_view(), name="chat"),
]

handler404 = pagenotfound
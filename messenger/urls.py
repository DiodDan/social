from django.urls import path
from .views import *


urlpatterns = [
    path("<str:login>", messenger.as_view(), name="messenger_page"),
]

handler404 = pagenotfound
from django.urls import path
from .views import *


urlpatterns = [
    path("", Search.as_view(), name="search"),
]

handler404 = pagenotfound

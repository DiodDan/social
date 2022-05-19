from django.urls import path
from .views import *


urlpatterns = [
    path("", Feed.as_view(), name="feed"),
]


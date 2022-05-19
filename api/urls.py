from django.urls import path
from .views import *


urlpatterns = [
    path("<str:login>", get_info.as_view(), name="chat"),
]

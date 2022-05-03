from django.http import HttpResponse
from django.views.generic import TemplateView
# from .forms import *
from profile.models import User, Message, Chat
from jinja2 import Environment, FileSystemLoader
from django.shortcuts import redirect
from django.http import JsonResponse


class get_info(TemplateView):
    def get(self, request, login):
        users = User.objects
        user = users.get(login=login)
        return JsonResponse(user.json_data(), safe=False)




def pagenotfound(reqest, exception):
    return HttpResponse(f"<h1>Либо ты проебався либо я еблан;(</h1>")
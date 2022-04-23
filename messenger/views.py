from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
#from .forms import *
from Profile.models import User, Message


class messenger(TemplateView):
    template_name = "messenger/main/messenger_page.html"

    def get(self, request, login):
        db = User.objects
        obj = db.get(login=login)
        messages = Message.objects
        return render(request, self.template_name, context={"obj": obj, "messages": messages.all(), "is_owner": (login == request.session["logedacc"])})

def pagenotfound(reqest, exception):
    return HttpResponse(f"<h1>Либо ты проебався либо я еблан;(</h1>")
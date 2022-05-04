from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from profile.models import User, Message, Chat
from jinja2 import Environment, FileSystemLoader


class Search(TemplateView):
    template_name = "search.html"
    template = Environment(loader=FileSystemLoader('templates')).get_template(template_name)

    def get(self, request):
        return HttpResponse(self.template.render(users_found=[],
                                                 logedacc=request.session["logedacc"],
                                                 csrf=request.COOKIES["csrftoken"]))

    def post(self, request):
        post = request.POST
        login = request.session["logedacc"]
        users = User.objects
        users_found = list(users.filter(name__contains=post["search_text"]))
        users_found += list(users.filter(login__contains=post["search_text"]))
        users_found += list(users.filter(email__contains=post["search_text"]))
        users_found = set(users_found)
        return HttpResponse(self.template.render(users_found=users_found,
                                                 logedacc=request.session["logedacc"],
                                                 csrf=request.COOKIES["csrftoken"]))

def pagenotfound(reqest, exception):
    return HttpResponse(f"<h1>Либо ты ... либо я ...;(</h1>")

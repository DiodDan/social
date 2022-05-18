from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from profile.models import User, Message, Chat
from jinja2 import Environment, FileSystemLoader, select_autoescape

autoescape = select_autoescape(enabled_extensions=('html', 'htm', 'xml'),
                             disabled_extensions=(),
                             default_for_string=True,
                             default=False)
class Search(TemplateView):
    template_name = "search.html"
    template = Environment(loader=FileSystemLoader('templates'), autoescape=autoescape).get_template(template_name)

    def get(self, request):
        login = request.session["logedacc"]
        users = User.objects
        users_found = set(users.all())
        return HttpResponse(self.template.render(users_found=users_found,
                                                 logedacc=login,
                                                 csrf=request.COOKIES["csrftoken"]))

    def post(self, request):
        pass

def pagenotfound(reqest, exception):
    return HttpResponse(f"<h1>Либо ты ... либо я ...;(</h1>")

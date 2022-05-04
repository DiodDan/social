from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from profile.models import User, Message, Chat


class Search(TemplateView):
    template_name = "search.html"

    def get(self, request):
        return render(request, self.template_name, context={})

    def post(self, request):
        post = request.POST
        login = request.session["logedacc"]
        users = User.objects
        users_found = users.filter(name__contains=post["search_text"])
        return render(request, self.template_name, context={"users_found": users_found})

def pagenotfound(reqest, exception):
    return HttpResponse(f"<h1>Либо ты ... либо я ...;(</h1>")

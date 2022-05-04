from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from profile.models import User, Message, Chat, Publication
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from django.shortcuts import redirect


class Feed(TemplateView):
    template_name = "feed.html"
    template = Environment(loader=FileSystemLoader('templates')).get_template(template_name)

    def get(self, request):
        login = request.session["logedacc"]
        users = User.objects
        user = users.get(login=login)
        publication = Publication.objects
        if user.follows:
            publications = publication.filter(author__in=user.follows.split(','))
        else:
            publications = []
        users_for_publications = []
        for publication in publications:
            users_for_publications.append(users.get(id=publication.author))
        lencomments = []
        lenlikes = []
        for publo in range(len(publications)):
            if publications[publo].comment_ids == '':
                lencomments.append(0)
            else:
                lencomments.append(len(publications[publo].comment_ids.split(",")))

            if publications[publo].like_ids == '':
                lenlikes.append(0)
            else:
                lenlikes.append(len(publications[publo].like_ids.split(",")))
        user.id = str(user.id)
        return HttpResponse(self.template.render(publications=publications,
                                                 users=users_for_publications,
                                                 user=user,
                                                 lenpublications=len(publications),
                                                 lencomments=lencomments,
                                                 lenlikes=lenlikes,
                                                 logedacc=request.session["logedacc"],
                                                 csrf=request.COOKIES["csrftoken"]))

    def post(self, request):
        post = request.POST
        login = request.session["logedacc"]
        users = User.objects
        user = users.get(login=login)
        publication = Publication.objects
        publication.create(image=request.FILES["image"], text=post["message"], author=user.id, time_created=":".join(str(datetime.now()).split()[1].split(":")[:2]))
        return redirect("/feed/")


def pagenotfound(reqest, exception):
    return HttpResponse(f"<h1>Либо ты ... либо я ...;(</h1>")

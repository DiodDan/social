from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import *
from profile.models import User, Message, Chat, Publication
from .email_sender import send_submit_email
from django.core.exceptions import ObjectDoesNotExist
from jinja2 import Environment, FileSystemLoader
import hashlib  as hash

FLAG = "1h2j45jlk?>gb;3445m5_+3"


class login(TemplateView):
    template_name = "login.html"

    def get(self, request):
        form = login_form()
        request.session["logedacc"] = ""
        return render(request, self.template_name, context={"form": form, "ERR": ""})

    def post(self, request):
        post = request.POST
        db = User.objects
        form = login_form(request.POST)
        user_data = db.filter(email=post["username"])

        if len(user_data) != 0 and str(user_data[0].password) == str(hash.sha256(post["password"].encode()).hexdigest()):
            request.session["logedacc"] = str(user_data[0].login)
            return redirect(f"/profile/{user_data[0].login}")
        else:
            return render(request, self.template_name, context={"form": form, "ERR": "Неверный пароль или логин"})


class signup(TemplateView):
    template_name = "login.html"

    def get(self, request):
        form = register_form()
        request.session["logedacc"] = ""
        return render(request, self.template_name,
                      context={"form": form, "ERR": ""})

    def post(self, request):
        post = request.POST
        db = User.objects
        form = register_form(request.POST)
        if len(db.filter(email=post["username"])) == 0:

            if post["password"] == post["repit_password"]:
                request.session["password"] = post["password"]
                request.session["repit_password"] = post["repit_password"]
                request.session["email"] = post["username"]

                return redirect(
                    f"/profile/submit_email/{post['username']}")
            else:
                return render(request, self.template_name,
                                  context={"form": form,
                                           "ERR": "Не совпадают пароли"})
        else:
            return render(request, self.template_name,
                          context={"form": form, "ERR": "Пользователь с такой почтой уже существует!!!"})


class submit_email(TemplateView):
    template_name = "email_submittion.html"
    token = {}

    def get(self, request, login):
        if login not in self.token.keys():
            self.token[login] = send_submit_email(login)
        return render(request, self.template_name, context={"ERR": "", "email": login})

    def post(self, request, login):
        post = request.POST
        users = User.objects
        try:
            if str(self.token[login]) == post["token"]:
                users.create(email=request.session["email"], password=hash.sha256(request.session["password"].encode()).hexdigest(),
                      profile_photo="photos/profile_photos/default.png",
                      description="")
                user = users.get(email=request.session["email"])
                user.login = user.pk
                user.name = "Диод"
                user.save()
                request.session["logedacc"] = str(user.login)
                del self.token[login]
                return redirect(f"/profile/{str(user.login)}")
            else:
                return render(request, self.template_name, context={"ERR": "Пароли не совпадают", "email": login})
        except:
            return "Ошибка"


class profile(TemplateView):
    template_name = "profile.html"
    template = Environment(loader=FileSystemLoader('templates')).get_template(template_name)
    themes = [{"color": "", },
              {"color": "red", "pic_path": "media/theme_photos/anonymous-cyber-crime-criminal-hack-hacker-svgrepo-com.svg"}]

    def get(self, request, login):
        try:
            users = User.objects
            user = users.get(login=login)
            user.followers = len([i for i in user.followers.split(",") if i != ''])
            user.follows = len([i for i in user.follows.split(",") if i != ''])
            publication = Publication.objects
            publications = publication.filter(author=user.id)
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
            self_user_id = str(users.get(login=request.session["logedacc"]).id)
            if login == request.session["logedacc"]:
                return HttpResponse(self.template.render(publications=publications,
                                                         user=user,
                                                         lenpublications=len(publications),
                                                         lencomments=lencomments,
                                                         lenlikes=lenlikes,
                                                         csrf=request.COOKIES["csrftoken"],
                                                         is_owner=True,
                                                         change_page=f"/profile/changedata/{user.login}",
                                                         logedacc=request.session["logedacc"],
                                                         is_subscribed=False,
                                                         theme_color=self.themes[user.used_theme]['color'],
                                                         self_user_id=self_user_id))
            else:
                return HttpResponse(self.template.render(publications=publications,
                                                         user=user,
                                                         lenpublications=len(publications),
                                                         lencomments=lencomments,
                                                         lenlikes=lenlikes,
                                                         csrf=request.COOKIES["csrftoken"],
                                                         is_owner=False,
                                                         logedacc=request.session["logedacc"],
                                                         is_subscribed=(str(user.id) in users.get(login=request.session["logedacc"]).follows.split(",")),
                                                         theme_color=self.themes[user.used_theme]['color'],
                                                         self_user_id=self_user_id))
        except Exception:
            return redirect("/profile/login/")

    def post(self, request, login):
        publications = Publication.objects
        post = request.POST
        if post["type"] == "delete_post":
            publications.get(id=post["post_id"]).delete()
        return redirect(f"/profile/{login}")

class changedata(TemplateView):
    template_name = "changedata.html"

    def get(self, request, login):

        obj = User.objects.get(login=login)
        form = change_data_form(
            {"login": obj.login, "name": obj.name,
             "description": obj.description, "photo": obj.profile_photo,
             "email": obj.email, "password": obj.password,
             "profile_photo": obj.profile_photo})
        return render(request, self.template_name,
                      context={"form": form, "obj": obj, "ERR": ""})

    def post(self, request, login):
        post = request.POST
        obj = User.objects.get(login=login)
        form = change_data_form(request.POST, request.FILES)
        if FLAG == post["flag_submit"]:
            obj.flags_found = "1"
            obj.save()
        if len(User.objects.filter(
                login=post["login"])) >= 1 and User.objects.get(
                login=post["login"]) != obj:
            return render(request, self.template_name,
                          context={"form": form, "obj": obj,
                                   "ERR": "Не уникальный логин"})
        else:
            obj.name = post["name"]
            obj.login = post["login"]
            obj.description = post["description"]
            obj.email = post["email"]
            if post["password"]:
                obj.password = hash.sha256(post["password"].encode()).hexdigest()
            if request.FILES.get("profile_photo"):
                obj.profile_photo = request.FILES["profile_photo"]
            obj.save()
            request.session["logedacc"] = str(obj.login)
            return redirect(f"/profile/{obj.login}")


class redir(TemplateView):
    def get(self, request):
        return redirect("/profile/login/")


def pagenotfound(reqest, exception):
    return HttpResponse(f"<h1>Либо ты ... либо я ...;(</h1>")

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import *
from profile.models import User, Message, Chat
from .email_sender import send_submit_email


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

        if len(user_data) != 0 and str(user_data[0].password) == str(post["password"]):
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
        if str(self.token[login]) == post["token"]:
            users.create(email=request.session["email"], password=request.session["password"],
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


class profile(TemplateView):
    template_name = "profile.html"
    themes = [{"color": "", },
              {"color": "red", "pic_path": "media/theme_photos/anonymous-cyber-crime-criminal-hack-hacker-svgrepo-com.svg"}]

    def get(self, request, login):
        users = User.objects
        user = users.get(login=login)
        user.followers = len([i for i in user.followers.split(",") if i != ''])
        user.follows = len([i for i in user.follows.split(",") if i != ''])
        if login == request.session["logedacc"]:
            return render(request, self.template_name,
                          context={"is_owner": True, "user": user,
                                   "change_page": f"/profile/changedata/{user.login}",
                                   "logedacc": request.session["logedacc"],
                                   "is_subscribed": False, "theme_color": self.themes[user.used_theme]['color']})
        else:
            return render(request, self.template_name,
                          context={"is_owner": False, "user": user,
                                   "logedacc": request.session["logedacc"],
                                   "is_subscribed": (str(user.id) in users.get(login=request.session["logedacc"]).follows.split(",")),
                                   "theme_color": self.themes[user.used_theme]['color']})


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
            obj.password = post["password"]
            if request.FILES.get("profile_photo"):
                obj.profile_photo = request.FILES["profile_photo"]
            obj.save()
            request.session["logedacc"] = str(obj.login)
            return redirect(f"/profile/{obj.login}")


class redir(TemplateView):
    def get(self, request):
        return redirect("/profile/login/")


def pagenotfound(reqest, exception):
    return HttpResponse(f"<h1>Либо ты проебався либо я еблан;(</h1>")

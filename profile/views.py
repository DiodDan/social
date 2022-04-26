from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import *
from profile.models import User, Message, Chat

class login(TemplateView):
    template_name = "login.html"

    def get(self, request):
        form = login_form()
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
        return render(request, self.template_name,
                      context={"form": form, "ERR": ""})

    def post(self, request):
        post = request.POST
        db = User.objects
        form = register_form(request.POST)
        if len(db.filter(email=post["username"])) == 0:

            if post["password"] == post["repit_password"]:
                db.create(email=post["username"], password=post["password"],
                          profile_photo="photos/profile_photos/defoult.png",
                          description="", followers=0, followed=0)
                obj = db.get(email=post['username'])
                obj.login = obj.pk
                obj.name = "Диод"
                obj.save()

                request.session["logedacc"] = str(obj.login)
                return redirect(
                    f"/profile/{db.get(email=post['username']).login}")
            else:
                return render(request, self.template_name,
                                  context={"form": form,
                                           "ERR": "Не совпадают пароли"})
        else:
            return render(request, self.template_name,
                          context={"form": form, "ERR": "Пользователь с такой почтой уже существует!!!"})

class profile(TemplateView):
    template_name = "profile.html"

    def get(self, request, login):

        obj = User.objects.get(login=login)
        if login == request.session["logedacc"]:
            return render(request, self.template_name,
                          context={"is_owner": True, "obj": obj,
                                   "change_page": f"/profile/changedata/{obj.login}"})
        else:
            return render(request, self.template_name,
                          context={"is_owner": False, "obj": obj})


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
            print(request.POST)
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
            return redirect(f"/profile/{obj.login}")


class redir(TemplateView):
    def get(self, request):
        return redirect("/profile/login/")


def pagenotfound(reqest, exception):
    return HttpResponse(f"<h1>Либо ты проебався либо я еблан;(</h1>")

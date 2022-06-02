from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import *
from profile.models import User, Message, Chat, Publication
from .email_sender import send_submit_email
from django.core.exceptions import ObjectDoesNotExist
from jinja2 import Environment, FileSystemLoader, select_autoescape
import hashlib as hash

FLAG = "1h2j45jlk?>gb;3445m5_+3"

autoescape = select_autoescape(enabled_extensions=('html', 'htm', 'xml'),
                               disabled_extensions=(),
                               default_for_string=True,
                               default=False)
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
        user_data = list(db.filter(email=post["username"])) + list(db.filter(login=post["username"]))

        if len(user_data) != 0 and str(user_data[0].password) == str(hash.sha256(post["password"].encode()).hexdigest()):
            request.session["logedacc"] = str(user_data[0].login)
            return redirect(f"/profile/{user_data[0].login}")
        else:
            return render(request, self.template_name, context={"form": form, "ERR": "incorrect login or password!"})


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

            request.session["password"] = post["password"]
            request.session["repit_password"] = post["repit_password"]
            request.session["email"] = post["username"]

            return redirect(
                f"/profile/submit_email/{post['username']}")
        else:
            return render(request, self.template_name,
                          context={"form": form, "ERR": "the user with this e-mail already exists!"})


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
                user.login = "diod" + hash.md5(str(user.pk).encode()).hexdigest()
                user.name = "diod"
                user.save()
                request.session["logedacc"] = str(user.login)
                del self.token[login]
                return redirect(f"/profile/{str(user.login)}")
            else:
                return render(request, self.template_name, context={"ERR": "token is incorrect", "email": login})
        except:
            return redirect("/")


class profile(TemplateView):
    template_name = "profile.html"
    template = Environment(loader=FileSystemLoader('templates'), autoescape=autoescape).get_template(template_name)

    user_not_found_template_name = "user_not_found.html"
    user_not_found_template = Environment(loader=FileSystemLoader('templates'), autoescape=autoescape).get_template(user_not_found_template_name)

    themes = [{"color": "", },
              {"color": "red", "pic_path": "media/theme_photos/anonymous.svg"}]

    def get(self, request, login):
        try:
            ERR = "user with this login already exists!" if request.GET.get("ERR", "") else ""
            users = User.objects
            user = users.get(login=login)
            user.followers = [i for i in user.followers.split(",") if i != '']
            user.follows = [i for i in user.follows.split(",") if i != '']

            followers = users.filter(id__in=user.followers)
            follows = users.filter(id__in=user.follows)

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
            try:
                self_user_id = str(users.get(login=request.session["logedacc"]).id)
            except ObjectDoesNotExist:
                return redirect("/login/")
            if login == request.session["logedacc"]:
                return HttpResponse(self.template.render(publications=publications,
                                                         user=user,
                                                         followers=followers,
                                                         follows=follows,
                                                         lenfollowers=len(user.followers),
                                                         lenfollows=len(user.follows),
                                                         lenpublications=len(publications),
                                                         lencomments=lencomments,
                                                         lenlikes=lenlikes,
                                                         csrf=request.COOKIES["csrftoken"],
                                                         is_owner=True,
                                                         change_page=f"/profile/changedata/{user.login}",
                                                         logedacc=request.session["logedacc"],
                                                         is_subscribed=False,
                                                         theme_color=self.themes[user.used_theme]['color'],
                                                         self_user_id=self_user_id,
                                                         email_shown=user.is_email_set_to_be_seen_or_not_by_user,
                                                         ERR=ERR))
            else:
                return HttpResponse(self.template.render(publications=publications,
                                                         user=user,
                                                         followers=followers,
                                                         follows=follows,
                                                         lenfollowers=len(user.followers),
                                                         lenfollows=len(user.follows),
                                                         lenpublications=len(publications),
                                                         lencomments=lencomments,
                                                         lenlikes=lenlikes,
                                                         csrf=request.COOKIES["csrftoken"],
                                                         is_owner=False,
                                                         logedacc=request.session["logedacc"],
                                                         is_subscribed=(str(user.id) in users.get(login=request.session["logedacc"]).follows.split(",")),
                                                         theme_color=self.themes[user.used_theme]['color'],
                                                         self_user_id=self_user_id,
                                                         email_shown=user.is_email_set_to_be_seen_or_not_by_user,
                                                         ERR=ERR))
        except KeyError:
            return redirect("/login/")

        except ObjectDoesNotExist:
            return HttpResponse(self.user_not_found_template.render())

    def post(self, request, login):
        publications = Publication.objects
        post = request.POST
        ERR = 0
        if post["type"] == "delete_post":
            publications.get(id=post["post_id"]).delete()
        if post["type"] == "change_data":
            obj = User.objects.get(login=login)
            if FLAG == post["flag_submit"]:
                obj.flags_found = "1"
                obj.save()
            if len(User.objects.filter(login=post["login"])) >= 1 and User.objects.get(login=post["login"]) != obj:
                ERR = 1
            else:
                ERR = 0
                obj.name = post["name"]
                obj.login = post["login"]
                obj.description = post["description"]
                obj.email = post["email"]
                if "set_email_visibility" in post.keys():
                    obj.is_email_set_to_be_seen_or_not_by_user = True
                else:
                    obj.is_email_set_to_be_seen_or_not_by_user = False
                if post["password"]:
                    obj.password = hash.sha256(post["password"].encode()).hexdigest()
                if request.FILES.get("profile_photo"):
                    obj.profile_photo = request.FILES["profile_photo"]
                obj.save()
                request.session["logedacc"] = str(obj.login)
                login = request.session["logedacc"]

        if ERR:
            return redirect(f"/profile/{login}?ERR={ERR}")
        else:
            return redirect(f"/profile/{login}")


class redir(TemplateView):
    def get(self, request):
        try:
            if request.session["logedacc"] == "":
                raise KeyError
            return redirect(f"/profile/{request.session['logedacc']}")
        except KeyError:
            return redirect("/login/")


def pagenotfound(reqest, exception):
    template_name = "page_not_found.html"
    template = Environment(loader=FileSystemLoader('templates'), autoescape=autoescape).get_template(template_name)
    return HttpResponse(template.render())

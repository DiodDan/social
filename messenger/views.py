from django.http import HttpResponse
from django.views.generic import TemplateView
# from .forms import *
from profile.models import User, Message, Chat
from jinja2 import Environment, FileSystemLoader, select_autoescape
from django.shortcuts import redirect
import messenger.consumers as consumers


autoescape = select_autoescape(enabled_extensions=('html', 'htm', 'xml'),
                             disabled_extensions=(),
                             default_for_string=True,
                             default=False)
class chat(TemplateView):
    template_name = "messenger.html"
    template = Environment(loader=FileSystemLoader('templates'), autoescape=autoescape).get_template(template_name)

    def get(self, request):
        login = request.session["logedacc"]
        if login == '':
            return redirect("/")
        users = User.objects
        user = users.get(login=login)
        consumers.group_members = list(set(consumers.group_members + [user.id]))
        messages = Message.objects
        chats = Chat.objects
        chats_for_user = []
        for chat in chats.all():
            if str(user.id) in chat.users.split(","):
                chats_for_user.append(chat)
        chat_messages = []
        for chat_obj in chats_for_user:
            chat_messages.append([])
            for message in messages.all():
                if str(message.id) in chat_obj.message_ids.split(","):
                    chat_messages[-1].append(message)
        unread_messages = []
        for chat_obj in chat_messages:
            unread_messages.append([])
            for message in chat_obj:
                if str(user.id) not in message.read_by.split(','):
                    unread_messages[-1].append(message)

        chat_users = {}
        users_for_chats = []
        for chat in chats_for_user:
            users_for_chats.append([])
            users_id_range = chat.users.split(",") + [24] if chat.name == "flags_chat" else chat.users.split(",")
            for u in users_id_range:
                t = users.get(id=u)
                chat_users[int(u)] = [t.name, t.login, t.profile_photo]
                users_for_chats[-1].append(t)
        follows = user.follows.split(',')
        followers = user.followers.split(',')
        friends = set(follows) & set(followers)
        friends = [users.get(id=i) for i in friends if i]
        users_for_chats_online = []
        for i in users_for_chats:
            users_for_chats_online.append(0)
            for j in i:
                if j.id in consumers.group_members:
                    users_for_chats_online[-1] += 1
        return HttpResponse(self.template.render(user=user,
                                                 messages=chat_messages,
                                                 is_owner=(request.session["logedacc"] == login),
                                                 chats=chats_for_user,
                                                 last_message=[[i[-1].text.split('<br>')[0] if len(i[-1].text.split('<br>')[0]) < 27 else i[-1].text[0:27].split('<br>')[0] + "...", i[-1].time_sent] if len(i) > 0 else ["", "Нет сообщений"] for i in chat_messages],
                                                 chats_len=len(chats_for_user),
                                                 chat_users=chat_users,
                                                 logedacc=request.session["logedacc"],
                                                 unread_messages=list(map(len, unread_messages)),
                                                 csrf=request.COOKIES["csrftoken"],
                                                 users_list=set(friends),
                                                 users_for_chats=list(map(set, users_for_chats)),
                                                 len_users_for_chats=list(map(len, users_for_chats)),
                                                 users_online=consumers.group_members,
                                                 users_for_chats_online=users_for_chats_online))

    def post(self, request):
        post = request.POST
        login = request.session["logedacc"]
        users = User.objects
        user = users.get(login=login)
        chats = Chat.objects
        if post["type"] == "create_chat":
            try:
                if post["chat_name"] == 'flags_chat':
                    chats.create(name=post["chat_name"], users=",".join(post.getlist("add_users") + [str(user.id)]), image=request.FILES["chat_image"], message_ids="17")
                else:
                    chats.create(name=post["chat_name"], users=",".join(post.getlist("add_users") + [str(user.id)]), image=request.FILES["chat_image"])
            except KeyError:
                if post["chat_name"] == 'flags_chat':
                    chats.create(name=post["chat_name"], users=",".join(post.getlist("add_users") + [str(user.id)]), image="../media/photos/profile_photos/default.png", message_ids="17")
                else:
                    chats.create(name=post["chat_name"], users=",".join(post.getlist("add_users") + [str(user.id)]), image="../media/photos/profile_photos/default.png")
        elif post["type"] == "edit_chat":
            chat = chats.get(id=post["chat_id"])
            chat.name = post["chat_name"]
            if request.FILES.get("chat_image"):
                chat.image = request.FILES["chat_image"]
            chat.users = ",".join(post.getlist("add_users"))
            if chat.users == "":
                chat.delete()
            else:
                chat.save()
        elif post["type"] == "delete_chat":
            chat = chats.get(id=post["chat_id"])
            chat.delete()
        return redirect("/messenger/")



def pagenotfound(reqest, exception):
    return HttpResponse(f"<h1>Либо ты ... либо я ...;(</h1>")

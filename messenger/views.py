from django.http import HttpResponse
from django.views.generic import TemplateView
# from .forms import *
from profile.models import User, Message, Chat
from jinja2 import Environment, FileSystemLoader


class chat(TemplateView):
    template_name = "messenger.html"
    template = Environment(loader=FileSystemLoader('templates')).get_template(template_name)


    def get(self, request, login):
        db = User.objects
        user = db.get(login=login)
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
        chat_users = {}
        for chat in chats.all():
            for u in chat.users.split(","):
                chat_users[int(u)] = db.get(id=u).name

        return HttpResponse(self.template.render(user=user,
                                    messages=chat_messages,
                                    is_owner=(request.session["logedacc"] == login),
                                    chats=chats_for_user,
                                    chat_ids=user.chat_ids.split(","),
                                    last_message=[[i[-1].text, i[-1].time_sent] if len(i) > 0 else "Нет сообщений" for i in chat_messages],
                                    chats_len=len(chats_for_user),
                                    chat_users=chat_users))


def pagenotfound(reqest, exception):
    return HttpResponse(f"<h1>Либо ты проебався либо я еблан;(</h1>")

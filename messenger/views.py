from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
#from .forms import *
from profile.models import User, Message, Chat


class chat(TemplateView):
    template_name = "messenger.html"

    def get(self, request, login):
        db = User.objects
        obj = db.get(login=login)
        messages = Message.objects
        chats = Chat.objects
        chat_obj = chats.get(id=chat_id)
        chats_for_user = []
        for chat in chats.all():
            if str(obj.id) in chat.users.split(","):
                chats_for_user.append(chat)
        chat_messages = []
        for message in messages.all():
            if str(message.id) in chat_obj.message_ids.split(","):
                chat_messages.append(message)
        return render(request, self.template_name, context={"obj": obj,
                                                            "messages": chat_messages,
                                                            "is_owner": True,
                                                            "chat_obj": chat_obj,
                                                            "chats": chats_for_user,
                                                            "chat_ids": obj.chat_ids.split(","),
                                                            "last_message": chat_messages[-1]})




def pagenotfound(reqest, exception):
    return HttpResponse(f"<h1>Либо ты проебався либо я еблан;(</h1>")

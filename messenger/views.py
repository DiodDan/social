from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
#from .forms import *
from profile.models import User, Message, Chat


class chat(TemplateView):

    template_name = "messenger.html"

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
        return render(request, self.template_name, context={"user": user,
                                                            "messages": chat_messages,
                                                            "is_owner": request.session["logedacc"] == login,
                                                            "chats": chats_for_user,
                                                            "chat_ids": user.chat_ids.split(","),
                                                            "last_message": [i[-1] for i in chat_messages]})




def pagenotfound(reqest, exception):
    return HttpResponse(f"<h1>Либо ты проебався либо я еблан;(</h1>")

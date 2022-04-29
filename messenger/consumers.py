import json
from channels.generic.websocket import WebsocketConsumer
from profile.models import User, Message, Chat
from asgiref.sync import async_to_sync
from datetime import datetime

class ChatConsumer(WebsocketConsumer):
    group_members = []

    def connect(self):
        users = User.objects
        self.user = users.get(login=self.scope["path"].split("/")[-2])
        self.group_members.append(self.user.id)
        self.group_members = list(set(self.group_members))
        self.room_group_name = self.scope["path"].split("/")[-1]
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "message":
            message, login, chat_id = text_data_json["message"], text_data_json["login"], self.scope["path"].split("/")[-1]
            messages = Message.objects
            t = str(datetime.now()).split()[1].split(":")[:2]
            user_id = User.objects.get(login=login).id
            message_obj = messages.create(autor=self.user.id, is_read=False, read_by=user_id, image="", text=message, time_sent=":".join(t))
            chats = Chat.objects
            chat_obj = chats.get(id=chat_id)
            chat_obj.message_ids = str(chat_obj.message_ids) + "," + str(message_obj.id) if str(chat_obj.message_ids) != "" else str(message_obj.id)
            chat_obj.save()
            chat_users = {}
            for chat in chats.all():
                for u in chat.users.split(","):
                    chat_users[int(u)] = User.objects.get(id=u).name
            chat_messages = []
            for msg in messages.all():
                if str(msg.id) in chat_obj.message_ids.split(","):
                    chat_messages.append(msg)
            unread_messages = []
            for member in self.group_members:
                unread_messages.append([])
                for msg in chat_messages:
                    if str(member) not in msg.read_by.split(','):
                        unread_messages[-1].append(msg)
            temp = {}
            for i in range(len(unread_messages)):
                temp[str(self.group_members[i])] = str(len(unread_messages[i]))
            unread_messages = temp
            del temp
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "login": login,
                    "img": str(self.user.profile_photo),
                    "time_sent": message_obj.time_sent,
                    "is_read": str(message_obj.is_read),
                    "chat_users": chat_users,
                    "user_id": user_id,
                    "chat": str(int(self.room_group_name)),
                    "unread_messages": unread_messages
                }
            )
        elif text_data_json["type"] == "messages_read":
            login, chat_id = text_data_json["login"], self.scope["path"].split("/")[-1]
            chats = Chat.objects
            messages = Message.objects
            users = User.objects
            chat_obj = chats.get(id=chat_id)

            user_id = users.get(login=login).id
            for message in messages.all():
                if str(message.id) in chat_obj.message_ids.split(","):
                    message.is_read = True
                    message.read_by = ",".join(set([i for i in message.read_by.split(",") if i != ''] + [str(user_id)]))
                    message.save()

    def chat_message(self, e):
        self.send(text_data=json.dumps({
            "type": "message",
            "message": e["message"],
            "login": e["login"],
            "img": e["img"],
            "time_sent": e["time_sent"],
            "is_read": e["is_read"],
            "chat_users": e["chat_users"],
            "user_id": e["user_id"],
            "chat": e["chat"],
            "unread_messages": e["unread_messages"]
            }))


class ProfileConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        users = User.objects
        self.self_user_login = self.scope["path"].split("/")[-2]
        self.other_user = users.get(login=self.scope["path"].split("/")[-1])


    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        if self.self_user_login != "":
            users = User.objects
            self.self_user = users.get(login=self.self_user_login)
            if self.other_user.login in self.self_user.follows.split(","):
                self.other_user.followers = self.other_user.followers.replace(self.self_user.login, "").replace(",,", ",").lstrip(",").rstrip(",")
                self.self_user.follows = self.self_user.follows.replace(self.other_user.login, "").replace(",,", ",").lstrip(",").rstrip(",")
                self.other_user.save()
                self.self_user.save()
            else:
                self.other_user.followers = ",".join(set([i for i in self.other_user.followers.split(",") if i != ''] + [str(self.self_user.id)]))
                self.self_user.follows = ",".join(set([i for i in self.self_user.follows.split(",") if i != ''] + [str(self.other_user.id)]))
                self.other_user.save()
                self.self_user.save()
            self.send(text_data=json.dumps({
                "type": "follow",
                'followers': len([i for i in self.other_user.followers.split(",") if i != '']),
                'follows': (str(self.other_user.login) in users.get(login=self.self_user.login).follows.split(","))
            }))
        else:
            self.send(text_data=json.dumps({
                "type": "error",
                "msg": "Вы должны войти в аккаунт!!!"
            }))

    def follow(self, e):
        self.send(text_data=json.dumps({
            "followers": e['followers'],
            "follows": e['follows']
            }))
import json
from channels.generic.websocket import WebsocketConsumer
from profile.models import User, Message, Chat
from asgiref.sync import async_to_sync
from datetime import datetime
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        users = User.objects
        self.user = users.get(login=self.scope["path"].split("/")[-2])
        self.room_group_name = self.scope["path"].split("/")[-1]
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "message":
            message, login, chat_id = text_data_json["message"], text_data_json["url"].split("/")[-1], self.scope["path"].split("/")[-1]
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
                    "chat": str(int(self.room_group_name) - 1)
                }
            )
        elif text_data_json["type"] == "messages_read":
            login, chat_id = text_data_json["url"].split("/")[-1], self.scope["path"].split("/")[-1]
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
            "chat": e["chat"]
            }))

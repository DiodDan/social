import json
from channels.generic.websocket import WebsocketConsumer
from profile.models import User, Message, Chat
from asgiref.sync import async_to_sync


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
        message, login, chat_id = text_data_json["message"], text_data_json["url"].split("/")[-2], text_data_json["url"].split("/")[-1]
        messages = Message.objects
        message_obj = messages.create(autor=self.user.id, is_read=False, read_by="", image="", text=message)
        chats = Chat.objects
        chat_obj = chats.get(id=chat_id)
        chat_obj.message_ids = str(chat_obj.message_ids) + "," + str(message_obj.id) if str(chat_obj.message_ids) != "" else str(message_obj.id)
        chat_obj.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "login": login,
                "img": str(self.user.profile_photo),
                "time_sent": str(str(message_obj.time_sent).split()[1].split(".")[0]),
                "is_read": str(message_obj.is_read)
            }
        )

    def chat_message(self, e):
        self.send(text_data=json.dumps({
            "type": "message",
            "message": e["message"],
            "login": e["login"],
            "img": e["img"],
            "time_sent": e["time_sent"],
            "is_read": e["is_read"]
            }))
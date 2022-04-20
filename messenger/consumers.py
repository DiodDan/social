import json
from channels.generic.websocket import WebsocketConsumer
from Profile.models import User, Message
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "test"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message, login = text_data_json["message"], text_data_json["url"].split("/")[-1]
        users = User.objects
        obj = users.get(login=login)
        messages = Message.objects
        messages.create(autor=obj.pk, is_read=False, read_by="", image="", text=message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )

    def chat_message(self, e):
        message = e["message"]

        self.send(text_data=json.dumps({
            "type": "message",
            "message": message
            }))

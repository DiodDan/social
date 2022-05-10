import json
from channels.generic.websocket import WebsocketConsumer

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coolsite.settings')

import django
django.setup()

from profile.models import User, Message, Chat, Publication

from asgiref.sync import async_to_sync
from datetime import datetime

group_members = []


# def get_online_users(login):
#     global group_members
#     users_for_chats = []
#     chats_for_user = []
#     users = User.objects
#     user = users.get(login=login)
#     chats = Chat.objects
#     for chat in chats.all():
#         if str(user.id) in chat.users.split(","):
#             chats_for_user.append(chat)
#     for chat in chats_for_user:
#         users_for_chats.append([chat])
#         for u in chat.users.split(","):
#             t = users.get(id=u)
#             users_for_chats[-1].append(t)
#     users_for_chats_online = {}
#     for i in users_for_chats:
#         users_for_chats_online[i[0].id] = 0
#         for j in i[1:]:
#             if j.id in group_members:
#                 users_for_chats_online[i[0].id] += 1
#     return users_for_chats_online


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        global group_members
        self.accept()
        users = User.objects
        self.user = users.get(login=self.scope["path"].split("/")[-2])
        group_members.append(self.user.id)
        group_members = list(set(group_members))
        self.room_group_name = self.scope["path"].split("/")[-1]
        # users_for_chats_online = get_online_users(self.user.login)

        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         "type": "online_users_reboot",
        #         "users_for_chats_online": users_for_chats_online
        #     }
        # )
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

    # def online_users_reboot(self, e):
    #     self.send(text_data=json.dumps({
    #         "type": "set_users_online",
    #         "users_for_chats_online": e["users_for_chats_online"],
    #     }))

    def receive(self, text_data):
        global group_members
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "message":
            message, login, chat_id = text_data_json["message"], text_data_json["login"], self.scope["path"].split("/")[-1]
            messages = Message.objects
            hour = str((datetime.now().hour + 3) % 24)
            hour = hour if len(hour) == 2 else '0' + hour
            minute = str(datetime.now().minute)
            minute = minute if len(minute) == 2 else '0' + minute
            t = hour + ":" + minute
            user_id = User.objects.get(login=login).id
            message_obj = messages.create(autor=self.user.id, is_read=False, read_by=user_id, image="", text=message.replace("\n", "<br>"), time_sent=t)
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
            for member in group_members:
                unread_messages.append([])
                for msg in chat_messages:
                    if str(member) not in msg.read_by.split(','):
                        unread_messages[-1].append(msg)
            temp = {}
            for i in range(len(unread_messages)):
                temp[str(group_members[i])] = str(len(unread_messages[i]))
            unread_messages = temp
            del temp

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message.replace("\n", "<br>"),
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

    def disconnect(self, close_code):
        global group_members

        try:
            users = User.objects
            group_members.remove(users.get(login=self.scope["path"].split("/")[-2]).id)
            # login = self.scope["path"].split("/")[-2]
            # users_for_chats_online = get_online_users(login)
            # async_to_sync(self.channel_layer.group_send)(
            #     self.room_group_name,
            #     {
            #         "type": "online_users_reboot",
            #         "users_for_chats_online": users_for_chats_online
            #     }
            # )
        except:
            pass


class ProfileConsumer(WebsocketConsumer):
    def connect(self):
        global group_members
        self.accept()
        users = User.objects
        chats = Chat.objects

        self.self_user_login = self.scope["path"].split("/")[-2]
        self.other_user = users.get(login=self.scope["path"].split("/")[-1])
        # users_for_chats_online = get_online_users(self.self_user_login)
        # user = users.get(login=self.self_user_login)
        # for chat in chats.all():
        #     if str(user.id) in chat.users.split(','):
        #         async_to_sync(self.channel_layer.group_send)(
        #             str(chat.id),
        #             {
        #                 "type": "online_users_reboot",
        #                 "users_for_chats_online": users_for_chats_online
        #             }
        #         )
        group_members.append(users.get(login=self.self_user_login).id)
        group_members = list(set(group_members))

    # def online_users_reboot(self, e):
    #     self.send(text_data=json.dumps({
    #         "type": "set_users_online",
    #         "users_for_chats_online": e["users_for_chats_online"],
    #     }))

    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        if self.self_user_login != "":
            users = User.objects
            self.self_user = users.get(login=self.self_user_login)
            if str(self.other_user.id) in self.self_user.follows.split(","):
                self.other_user.followers = self.other_user.followers.replace(str(self.self_user.id), "").replace(",,", ",").lstrip(",").rstrip(",")
                self.self_user.follows = self.self_user.follows.replace(str(self.other_user.id), "").replace(",,", ",").lstrip(",").rstrip(",")
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
                'follows': (str(self.other_user.id) in users.get(login=self.self_user.login).follows.split(","))
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

    def disconnect(self, close_code):
        global group_members
        users = User.objects
        chats = Chat.objects
        group_members.remove(users.get(login=self.scope["path"].split("/")[-2]).id)
        # login = self.scope["path"].split("/")[-2]
        # users_for_chats_online = get_online_users(login)
        # user = users.get(login=self.self_user_login)
        # for chat in chats.all():
        #     if str(user.id) in chat.users.split(','):
        #         async_to_sync(self.channel_layer.group_send)(
        #             str(chat.id),
        #             {
        #                 "type": "online_users_reboot",
        #                 "users_for_chats_online": users_for_chats_online
        #             }
        #         )


class LikeConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "like":
            print(text_data_json["user_login"])
            user_id = User.objects.get(login=text_data_json["user_login"]).id
            post_id = text_data_json["post_id"]
            publications = Publication.objects
            post = publications.get(id=post_id)
            post.like_ids = post.like_ids + ',' + str(user_id)
            if post.like_ids[0] == ',':
                post.like_ids = post.like_ids[1:]
            post.save()
        elif text_data_json["type"] == "unlike":
            user_id = User.objects.get(login=text_data_json["user_login"]).id
            post_id = text_data_json["post_id"]
            publications = Publication.objects
            post = publications.get(id=post_id)
            p = post.like_ids.split(',')
            p.remove(str(user_id))
            post.like_ids = ','.join(p)
            post.save()

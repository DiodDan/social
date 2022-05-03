from django.db import models


class User(models.Model):
    login = models.CharField(max_length=15, verbose_name="Логин")
    email = models.EmailField(max_length=40, verbose_name="Почта")
    password = models.CharField(max_length=30, verbose_name="Пароль")
    name = models.CharField(max_length=30, verbose_name="Имя")
    description = models.CharField(max_length=300, verbose_name="Описание")
    chat_ids = models.CharField(max_length=300)
    followers = models.TextField(verbose_name="followers", blank=True)
    follows = models.TextField(verbose_name="follows", blank=True)
    profile_photo = models.ImageField(upload_to="photos/profile_photos", verbose_name="Фото аккаунта", blank=True)
    flags_found = models.TextField(verbose_name="flags_found", blank=True)
    used_theme = models.IntegerField(verbose_name="used_theme", default="0")

    def get_list(self, lst):
        if lst == '':
            return list()
        lst = lst.split(',')
        return sorted(list(map(int, lst)))

    def json_data(self):
        return {"login": self.login,
                "email": self.email,
                "name": self.name,
                "description": self.description,
                "chat_ids": self.get_list(self.chat_ids),
                "followers": self.get_list(self.followers),
                "follows": self.get_list(self.follows),
                "flags_found": self.get_list(self.flags_found),
                "used_theme": self.used_theme}


class Message(models.Model):
    time_sent = models.CharField(max_length=10, verbose_name="time_sent")
    autor = models.IntegerField(verbose_name="autor")
    is_read = models.BooleanField(verbose_name="is_read")
    read_by = models.CharField(max_length=150, verbose_name="read_by")
    text = models.CharField(max_length=1000, verbose_name="text")
    image = models.ImageField(upload_to="photos/chat_images", verbose_name="image", blank=True)


class Chat(models.Model):
    name = models.CharField(max_length=40, verbose_name="name")
    users = models.CharField(max_length=150, verbose_name="users")
    image = models.ImageField(upload_to="photos/chat_images",
                              verbose_name="image", blank=True)
    message_ids = models.TextField(verbose_name="message_ids")

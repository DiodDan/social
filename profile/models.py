from django.db import models


class User(models.Model):
    login = models.CharField(max_length=15, verbose_name="Логин")
    email = models.CharField(max_length=40, verbose_name="Почта")
    password = models.CharField(max_length=30, verbose_name="Пароль")
    name = models.CharField(max_length=30, verbose_name="Имя")
    description = models.CharField(max_length=300, verbose_name="Описание")
    chat_ids = models.CharField(max_length=300)

    profile_photo = models.ImageField(upload_to="photos/profile_photos", verbose_name="Фото аккаунта", blank=True)


class Message(models.Model):
    time_sent = models.DateTimeField(auto_now=True, verbose_name="time_sent")
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

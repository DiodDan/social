from django.db import models


class User(models.Model):
    login = models.CharField(max_length=15, verbose_name="Логин")
    email = models.CharField(max_length=40, verbose_name="Почта")
    password = models.CharField(max_length=30, verbose_name="Пароль")
    name = models.CharField(max_length=30, verbose_name="Имя")
    description = models.CharField(max_length=300, verbose_name="Описание")
    chat_ids = models.CharField(max_length=300)

    profile_photo = models.ImageField(upload_to="photos/profile_photos", verbose_name="Фото аккаунта", blank=True)

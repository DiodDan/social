from django.db import models


class User(models.Model):
    login = models.CharField(max_length=15, verbose_name="Логин")
    email = models.EmailField(max_length=40, verbose_name="Почта")
    password = models.CharField(max_length=64, verbose_name="Пароль")
    name = models.CharField(max_length=30, verbose_name="Имя")
    description = models.CharField(max_length=300, blank=True, verbose_name="Описание")
    chat_ids = models.CharField(max_length=300, blank=True)
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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Message(models.Model):
    time_sent = models.CharField(max_length=10, verbose_name="Время отправки")
    autor = models.IntegerField(verbose_name="Автор")
    is_read = models.BooleanField(verbose_name="Прочитано")
    read_by = models.CharField(max_length=150, verbose_name="Кем прочитано")
    text = models.CharField(max_length=1000, verbose_name="Сообщение")
    image = models.ImageField(upload_to="photos/chat_images", verbose_name="image", blank=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Chat(models.Model):
    name = models.CharField(max_length=40, verbose_name="Название")
    users = models.CharField(max_length=150, verbose_name="Участники")
    image = models.ImageField(upload_to="photos/chat_images",
                              verbose_name="Фото", blank=True)
    message_ids = models.TextField(verbose_name="ID сообщений")

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Publication(models.Model):
    author = models.IntegerField(verbose_name="Автор")
    text = models.TextField(verbose_name="Текст")
    image = models.ImageField(upload_to="photos/publication_images", blank=True, verbose_name="Фото")
    like_ids = models.TextField(blank=True, verbose_name="ID лайков")
    comment_ids = models.TextField(blank=True, verbose_name="ID сообщений")
    time_created = models.CharField(max_length=10, verbose_name="Время создания")

    class Meta:

        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

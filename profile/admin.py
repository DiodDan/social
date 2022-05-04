from django.contrib import admin

from .models import *

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'email', 'password', 'name', 'description')
    list_display_links = ('login', 'email', 'password', 'name', 'description')
    search_fields = ('login', 'email', 'password', 'name', 'description')


class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'users')
    list_display_links = ('name', 'users')
    search_fields = ('name', 'users')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('time_sent', 'text', 'autor')
    list_display_links = ('text', 'autor')
    search_fields = ('text', )


admin.site.register(User, UserAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
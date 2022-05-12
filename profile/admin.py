from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import *

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'email', 'password', 'name', 'description')
    search_fields = ('login', 'email', 'password', 'name', 'description')


class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'users')
    search_fields = ('name', 'users')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_sent', 'text', 'autor')
    search_fields = ('text', 'autor')

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('author', 'text')
    search_fields = ('author', 'text')

admin.site.register(User, UserAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Publication, PublicationAdmin)

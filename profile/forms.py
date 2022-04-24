from django import forms
from .models import *
class login_form(forms.Form):
    name = "signin"
    email = forms.EmailField(max_length=40, label="Username", widget=forms.TextInput(attrs={'placeholder': 'Login', "typr": "text"}))
    password = forms.CharField(max_length=30, label="Password", widget=forms.TextInput(attrs={'placeholder': 'Password', "type": "password"}))

class register_form(forms.Form):
    name = "signup"
    email = forms.EmailField(max_length=40, label="Username", widget=forms.TextInput(attrs={'placeholder': 'Login', "class": "text"}))
    password = forms.CharField(max_length=30, label="Password", widget=forms.TextInput(attrs={'placeholder': 'Password', "class": "text"}))
    repit_password = forms.CharField(max_length=30, label="Repeat password", widget=forms.TextInput(attrs={'placeholder': 'Repeat password', "class": "text"}))


class change_data_form(forms.Form):
    email = forms.CharField(max_length=40, label="email", required=False)
    password = forms.CharField(max_length=40, label="Пароль", required=False)
    description = forms.CharField(max_length=30, label="Описание аккаунта", required=False, widget=forms.Textarea())
    profile_photo = forms.FileField(widget=forms.FileInput(), required=False, label="Фото профиля")
    name = forms.CharField(max_length=40, label="Имя", required=False)
    login = forms.CharField(max_length=30, label="Логин", required=False)

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _


class MyUserCreationForm(UserCreationForm):
    class Meta:
        fields = ("username","email")
        field_classes = {
            'username': UsernameField,
            'email': EmailField,
        }
        model = User
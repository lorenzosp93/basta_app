from django.contrib import admin
from django.contrib.auth.models import User
from .models import Session, Round, Play 
# Register your models here.

admin.register(User)

admin.register(Session)
admin.register(Round)
admin.register(Play)
from django.contrib import admin
from .models import Session, Round, Play 
# Register your models here.

@admin.register(Session, Round, Play)
class BastaAppAdmin(admin.ModelAdmin):
    pass
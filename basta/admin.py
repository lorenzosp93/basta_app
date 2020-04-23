from django.contrib import admin
from .models import Session, Round, Play 
# Register your models here.

class AuditableAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'modified_by', 'created_at', 'modified_at')
    date_hierarchy = 'created_at'
    def save_model(self, request, obj, form, change):
        obj.save(user=request.user)
class RoundTabular(admin.TabularInline):
    model = Round
    extra = 5
        
@admin.register(Session)
class SessionAdmin(AuditableAdmin):
    inlines = [RoundTabular]
    list_display = ('name', 'active')

class PlayTabular(admin.TabularInline):
    model = Play
    extra = 5

@admin.register(Round)
class RoundAdmin(AuditableAdmin):
    inlines = [PlayTabular]
    list_display = (
        '__str__',
        'active',
        'created_by',
        'created_at'
    )

@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'score',
        'created_at',
        'modified_at'
    )
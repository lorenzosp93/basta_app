from django.contrib import admin
from .models import Session, Round, Play 
# Register your models here.

class AuditableAdmin(admin.ModelAdmin):
    exclude = ('created_by', 'modified_by', 'created_at', 'modified_at')
    def save_model(self, request, obj, form, change):
        obj.save(user=request.user)
        
@admin.register(Session)
class SessionAdmin(AuditableAdmin):
    pass
@admin.register(Round)
class RoundAdmin(AuditableAdmin):
    pass
@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    pass
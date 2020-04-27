"Module to define the base basta app models"
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils.text import slugify

class TimeStampable(models.Model):
    "Abstract model to define timestamp attributes"
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Modified at",
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]

class Named(models.Model):
    "Abstract model to define names and slugs"
    class Meta:
        abstract = True

    name = models.TextField(
        verbose_name=_("Session name"),
        max_length=50,
        blank=True,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        "Override save function to add default for name field and slugify"
        self.slug_name()
        super().save(*args, **kwargs)
        
    def slug_name(self):
        self.slug = slugify(self.get_name())
    
    def get_name(self):
        return self.name

class Auditable(TimeStampable):
    class Meta:
        abstract = True
    
    created_by = models.ForeignKey(
        User,
        related_name='+',
        on_delete=models.SET_NULL,
        null=True,
    )
    modified_by = models.ForeignKey(
        User,
        related_name='+',
        on_delete=models.SET_NULL,
        null=True,
    )

    def save(self, *args, **kwargs):
        try:
            user = self.user
        except:
            user = kwargs.pop('user', None)
        finally:
            if user:
                self.audit_fields_set(user)

        return super().save(*args, **kwargs)

    def audit_fields_set(self, user):
        if isinstance(user, User):
            if not self.created_by:
                self.created_by = user
            self.modified_by = user
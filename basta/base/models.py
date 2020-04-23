"Module to define the base basta app models"
from django.db import models
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
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        "Override save function to add default for name field and slugify"
        self.slug_name()
        super().save(*args, **kwargs)
        
    def slug_name(self):
        if not self.name:
            self.name =  _("Game on %(date)s" % {"date": now()})
        self.slug = slugify(self.name)

class Auditable(TimeStampable):
    class Meta:
        abstract = True
    
    created_by = models.ForeignKey(
        User,
        related_name='+',
        on_delete=models.DO_NOTHING,
    )
    modified_by = models.ForeignKey(
        User,
        related_name='+',
        on_delete=models.DO_NOTHING,
    )

    def save(self, **kwargs):
        if (user := **kwargs.pop('user', None)):
            self.audit_fields_set(user)
        return super().save(**kwargs)

    def audit_fields_set(self, user):
        if isinstance(user, User):
            if not self.created_by:
                self.created_by = self.user
            self.modified_by = self.user
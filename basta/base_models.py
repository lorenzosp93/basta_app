"Module to define the base basta app models"
from django.db import models

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

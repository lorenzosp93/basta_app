"Module to define the basta app models"
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import ValidationError

# Create your models here.

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


class Session(TimeStampable):
    "Model to define a play session, participants and rules"
    participants = models.ManyToManyField(
        User,
        verbose_name="Participants",
    )

    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")


class Round(models.Model):
    "Model to defind one round within a session"
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        verbose_name="Session"
    )
    letter = models.TextField(
        max_length=1,
        verbose_name="Letter",
    )

    def get_total_score(self):
        return sum([round_.score for round_ in self.round_set.all()])

    class Meta:
        verbose_name = _("Round")
        verbose_name_plural = _("Rounds")
        unique_together = ("letter", "session",)

def validate_letter(letter, word):
    if not word.startswith(letter):
                raise ValidationError(
                    _("%(w)s does not start with %(l)s"),
                    params={
                        "w": word,
                        "l": letter,
                    }
                )

class Play(models.Model):
    "Model to define one play for one user"
    cur_round = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        verbose_name="Name",
        max_length=15,
    )
    surname = models.CharField(
        verbose_name="Surname",
        max_length=15,
    )
    plant = models.CharField(
        verbose_name="Flower / Fruit / Vegetable",
        max_length=15,
    )
    animal = models.CharField(
        verbose_name="Animal",
        max_length=15,
    )
    place = models.CharField(
        verbose_name="City / Country",
        max_length=15,
    )
    film = models.TextField(
        max_length=40,
        verbose_name="Movie / Series",
    )
    obj = models.CharField(
        verbose_name="Object",
        max_length=15,
    )
    brand = models.CharField(
        verbose_name="Brand",
        max_length=15,
    )

    score = models.IntegerField(editable=False, default=0)

    def clean(self):
        "Define validations on word values"
        letter = self.cur_round.letter
        for category in ["name", "surname", "plant", "animal",
                         "place", "film", "object", "brand"]:
            word = self.__getattribute__(category)
            validate_letter(letter, word)

    def save(self):
        "Save the Play with the associated score for the user"

    class Meta:
        verbose_name = _("Play")
        verbose_name_plural = _("Plays")



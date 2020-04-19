"Module to define the basta app models"
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .utils import validate_letter
from .base_models import TimeStampable

# Create your models here.
class Session(TimeStampable):
    "Model to define a play session, participants and rules"
    participants = models.ManyToManyField(
        User,
        verbose_name=_("Participants"),
    )

    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")


class Round(models.Model):
    "Model to defind one round within a session"
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        verbose_name=_("Session")
    )
    letter = models.TextField(
        max_length=1,
        verbose_name=_("Letter"),
    )

    @property
    def get_scores(self):
        return {round_.user: round_.score 
                 for round_ in self.round_set.all()}

    @property
    def total_score(self):
        return sum(get_scores.values())

    class Meta:
        verbose_name = _("Round")
        verbose_name_plural = _("Rounds")
        unique_together = ("letter", "session",)

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
        verbose_name=_("Name"),
        max_length=15,
        blank=True,
    )
    surname = models.CharField(
        verbose_name=_("Surname"),
        max_length=15,
        blank=True,
    )
    plant = models.CharField(
        verbose_name=_("Flower / Fruit / Vegetable"),
        max_length=15,
        blank=True,
    )
    animal = models.CharField(
        verbose_name=_("Animal"),
        max_length=15,
        blank=True,
    )
    place = models.CharField(
        verbose_name=_("City / Country"),
        max_length=15,
        blank=True,
    )
    film = models.TextField(
        max_length=40,
        verbose_name=_("Movie / Series"),
        blank=True,
    )
    obj = models.CharField(
        verbose_name=_("Object"),
        max_length=15,
        blank=True,
    )
    brand = models.TextField(
        verbose_name=_("Brand"),
        max_length=25,
        blank=True,
    )

    score = models.IntegerField(editable=False, default=0)

    def clean(self):
        "Define validations on word values"
        letter = self.cur_round.letter
        for category in ["name", "surname", "plant", "animal",
                         "place", "film", "object", "brand"]:
            word = self.__getattribute__(category)
            validate_letter(letter, word)


    class Meta:
        verbose_name = _("Play")
        verbose_name_plural = _("Plays")



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

    @property
    def get_scores(self):
        return {round_user: round_.score 
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
    brand = models.TextField(
        verbose_name="Brand",
        max_length=25,
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



"Module to define the basta app models"
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils.timezone import now
from random import choice
import string
from .base.utils import validate_starts
from .base.models import TimeStampable

# Create your models here.

class Session(TimeStampable):
    "Model to define a play session, participants and rules"
    active = models.BooleanField(
        verbose_name=_("Is session active?"),
        default = True,
    )
    name = models.TextField(
        verbose_name=_("Session name"),
        max_length=50,
        blank=True,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    @property
    def n_rounds(self):
        return self.round_set.count()

    @property
    def participants(self):
        return set([r for round_ in self.round_set.all() for r in round_.participants])

    @property
    def get_scores(self):
        rounds_scores = [round_.get_scores for round_ in self.round_set.all()]
        participant_scores = {}
        for round_ in rounds_scores:
            for key, val in round_.items():
                if key not in participant_scores.keys():
                    participant_scores[key] = val
                else:
                    participant_scores[key] += val
        return participant_scores
    
    @property
    def get_winner_score(self):
        scores = self.get_scores
        if scores:
            winner = max(scores.keys(), key=(lambda key: scores[key]))
            return {winner: scores[winner]}
        else:
            return {}

    def save(self, *args, **kwargs):
        "Override save function to add default for name field and slugify"
        if not self.name:
            self.name =  _("Game on %(date)s" % {"date": now()})
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")


class Round(TimeStampable):
    "Model to defind one round within a session"
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        verbose_name=_("Session"),
        related_name="round_set"
    )
    number = models.PositiveIntegerField()
    letter = models.TextField(
        max_length=1,
        verbose_name=_("Letter"),
        editable=False,
        blank=True,
    )
    active = models.BooleanField(
        verbose_name=_("Is round active?"),
        default=True,
    )

    @property
    def participants(self):
        return set([play.user for play in self.play_set.all()])

    @property
    def get_scores(self):
        return {play.user.username: play.score 
                 for play in self.play_set.all()}
    
    @property
    def get_winner_score(self):
        scores = self.get_scores
        if scores:
            winner = max(scores.keys(), key=(lambda key: scores[key]))
            return {winner: scores[winner]}
        else:
            return {}
    
    def get_letter(self):
        taken_letters = self.session.round_set\
                            .all()\
                            .values_list('letter', flat=True)
        letters = list(string.ascii_lowercase)
        avail_letters = [l for l in letters if l not in taken_letters]
        return choice(avail_letters)

    def save(self, *args, **kwargs):
        "Override save function to calculate the round number"
        self.letter = self.get_letter()
        if self.pk == None:
            self.number = self.session.round_set.count() + 1
        super().save(*args, **kwargs)
    

    class Meta:
        verbose_name = _("Round")
        verbose_name_plural = _("Rounds")
        unique_together = ("letter", "session",)

class Play(TimeStampable):
    "Model to define one play for one user"
    round = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        related_name="play_set"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="play_set"
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

    score = models.PositiveIntegerField(editable=False, default=0)

    def clean(self):
        "Define validations on word values"
        self.play_validate_starts()

    def play_validate_starts(self):
        letter = self.round.letter
        for category in ["name", "surname", "plant", "animal",
                         "place", "film", "obj", "brand"]:
            word = self.__getattribute__(category)
            validate_starts(letter, word)
    class Meta:
        verbose_name = _("Play")
        verbose_name_plural = _("Plays")
        unique_together = ['round', 'user']

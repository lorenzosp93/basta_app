"Module to define the basta app models"
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
from django.utils.timezone import now
import random
import string
from .base.utils import validate_starts
from .base.models import Auditable, TimeStampable, Named

# Create your models here.

CATEGORIES = (
    ('name', _("Name")),
    ('surname', _("Surname")),
    ('plant', _("Flower / Fruit / Vegetable")),
    ('animal', _("Animal")),
    ('location', _("City / Country")),
    ('film', _("Movie / Series")),
    ('object', _("Object")),
    ('brand', _("Brand")),
    ('band', _("Musician / Band")),
    ('color', _("Color")),
    ('profession', _("Profession")),
    ('sport', _("Sport")),
    ('historical', _("Historical figure")),
    ('art', _("Monument / Art piece")),
    ('gifts', _("Gift / Present")),
    ('bad_habits', _("Bad habit")),
    ('reasons911', _("Reason to call 911")),
    ('food', _("Food")),
    ('athletes', _("Athlete")),
    ('fictional', _("Fictional character")),
    ('instruments', _("Instrument / Tool")),
    ('halloween', _("Halloween costume")),
    ('bodyparts', _("Body part")), # v1, migration 0014
    ('suicide', _('Dumb ways to die')),
    ('clothing', _('Cloting items')),
    ('drinks', _('Drink')),
    ('black', _('Thing that is black')),
    ('rivers', _('River')),
    ('boardgames', _('Board game')),
    ('author', _('Author')),
    ('song', _('Song')),
)
DEFAULTS = [
    'name', 'surname','plant', 'animal',
    'location', 'film', 'object', 'brand'
]

class Category(models.Model):
    name = models.CharField(
        verbose_name=_("Category name"),
        choices=CATEGORIES,
        unique=True,
        max_length=15,
    )
    default = models.BooleanField(
        verbose_name="Is default category?",
        default=False,
    )
    def __str__(self):
        return "<Category " + self.name +">"

class Session(Auditable, Named):
    "Model to define a play session, participants and rules"
    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")
        ordering = ['-created_at']

    active = models.BooleanField(
        verbose_name=_("Is session active?"),
        default = True,
    )

    categories = models.ManyToManyField(
        Category,
        related_name="+",
    )

    random_categories = models.BooleanField(
        verbose_name=_("Random categories"),
        default=False,
    )
    
    def get_absolute_url(self):
        return reverse("basta:session", kwargs={"slug": self.slug})

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
        return [
            {'participant': participant, 'score': score} 
            for participant, score in participant_scores.items()
        ]
    
    @property
    def get_winner_score(self):
        score_list = self.get_scores
        if score_list:
            winner = max(
                range(len(score_list)),
                key=lambda index: score_list[index]['score']
            )
            return {score_list[winner]['participant']: score_list[winner]['score']}
        else:
            return {}
    
    def get_name(self):
        if not self.name:
            self.name =  _("Game on %(date)s" % {"date": now()})
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.categories.all():
            self.categories.set(Category.objects.filter(default=True))

class Round(Auditable):
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

    def get_absolute_url(self):
        return reverse('basta:round', kwargs={
            'slug': self.session.slug,
            'number': self.number,
        })

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
        return random.choice(avail_letters)

    def save(self, *args, **kwargs):
        "Override save function to calculate the round number"
        if not self.letter:
            self.letter = self.get_letter()
        if self.number == None:
            self.set_number()
        super().save(*args, **kwargs)
        if not self.active:
            self.end_session_on_final_round()
    
    def set_number(self):
        self.number = self.session.round_set.count() + 1

    def end_session_on_final_round(self):
        try:
            self.get_letter()
        except:
            self.session.active = False
            self.session.save()

    def __str__(self):
        return f"Round {self.number} of {self.session.__str__()}"
    class Meta:
        verbose_name = _("Round")
        verbose_name_plural = _("Rounds")
        unique_together = ("letter", "session",)
        ordering = ['number']

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

    score = models.PositiveIntegerField(editable=False, default=0)

    def get_categories(self):
        random.seed(self.round.pk)
        if self.round.session.random_categories:
            return random.sample(list(Category.objects.all()) ,k=len(DEFAULTS))
        else:
            return self.round.session.categories.all()
    
    def create_playcategories(self):
        for category in self.get_categories():
            PlayCategory.objects.create(
                category=category,
                play=self,
            )

    def save(self, **kwargs):
        super().save(**kwargs)
        if not self.categories.all():
            self.create_playcategories()

    def get_absolute_url(self):
        return reverse("basta:play", kwargs={
            "slug": self.round.session.slug,
            "number": self.round.number,
        })
    
    def __str__(self):
        return f"{self.user}'s play of {self.round.__str__()}"
    class Meta:
        verbose_name = _("Play")
        verbose_name_plural = _("Plays")
        unique_together = ['round', 'user']
        ordering = ['score']

class PlayCategory(TimeStampable):
    "Model to define the fields in each play"
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        related_name="+"
    )
    play = models.ForeignKey(
        Play,
        on_delete=models.CASCADE,
        related_name="categories",
    )
    value = models.CharField(
        max_length = 50,
        blank=True,
    )

    @property
    def label(self):
        return self.category.get_name_display()

    def clean(self):
        "Define validations on word values"
        self.play_validate_starts()
        super().clean()

    def play_validate_starts(self):
        letter = self.play.round.letter
        if self.value:
            validate_starts(letter, self.value)
    
    def __str__(self):
        return "PlayCategory " + self.category.name + " of " + str(self.play)
    
    class Meta:
        ordering = ['play', 'category']
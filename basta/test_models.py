"Module to test the basta app models"
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.validators import ValidationError
from django.utils.crypto import get_random_string
from unittest import mock
from copy import copy
from .models import (
    Play,
    Round,
    Session,
    Category,
    PlayCategory
)

# Write your tests here

class TestBastaModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser1")
        self.category = Category.objects.get(
            name="name",
            default=True,
        )
        self.session = Session.objects.create(
            name='test session',
        )
        self.session.categories.set([self.category])
        self.round = Round.objects.create(
            session=self.session,
        )
        self.play = Play.objects.create(
            round=self.round,
            user=self.user,
        )
        

    def test_auditable(self):
        session = Session.objects.create(
            name = 'oldname',
            created_by = self.user
        )
        user2 = User.objects.create_user(username='testuser3')
        session.name = 'newname'
        session.save(user=user2)
        self.assertEqual(
            session.created_by,
            self.user,
        )
        self.assertEqual(
            session.modified_by,
            user2,
        )
    
    def test_named(self):
        self.assertEqual(self.session.slug, 'test-session')
    
    def test_session_create(self):
        self.assertIsInstance(self.session, Session)
    
    def test_round_create(self):
        self.assertIsInstance(self.round, Round)
        
    def test_play_create(self):
        self.assertIsInstance(self.play, Play)
    
    def test_playcategory_validate(self):
        play = copy(self.play)
        letter = play.round.letter
        playcategory = play.categories.first()
        playcategory.value = letter + 'test'
        playcategory.clean()
        next_letter = chr(ord(letter) + 1)
        wr_name = next_letter + 'test'
        playcategory.value = wr_name
        self.assertRaises(
            ValidationError,
            playcategory.clean)
    
    
    def set_up_plays(self, round_=None):
        if not round_:
            round_ = self.round
        play1 = copy(self.play)
        user2 = User.objects.create_user(username='testuser2')
        play2 = Play.objects.create(
            round=round_,
            user=user2,
        )
        playcat = PlayCategory.objects.create(
            play=self.play,
            category=self.category,
        )
        play1.categories.set([playcat])
        playcategory2 = PlayCategory.objects.create(
            play=play2,
            category=self.category
        )
        play2.categories.set([playcategory2])
        return play1, play2

    def set_up_scores(self, round_=None):
        if not round_:
            round_ = self.round
        play1, play2 = self.set_up_plays(round_)
        play1.score = 2
        play1.save()
        play2.score = 5
        play2.save()
        return play1, play2

    def test_round_participants(self):
        play1, play2 = self.set_up_plays()
        self.assertSetEqual(
            self.round.participants,
            set([play1.user, play2.user])
        )

    def test_round_get_scores(self):
        play1, play2 = self.set_up_scores()
        self.assertDictEqual(
            self.round.get_scores,
            {
                play1.user.username: 2,
                play2.user.username: 5,
            }
        )

    def test_round_get_winner_score(self):
        _, play2 = self.set_up_scores()
        self.assertDictEqual(
            self.round.get_winner_score,
            {play2.user.username: 5}
        )
    
    def set_up_rounds(self, session=None):
        if not session:
            session = self.session
        round1 = copy(self.round)
        round2 = Round.objects.create(
            session=session,
        )
        play3, play4 = self.set_up_plays(round2)
        return round1, round2
    
    def set_up_letters(self, session=None):
        if not session:
            session = self.session
        round1, round2 = self.set_up_rounds(session)
        round1.save()
        round2.save()
        return round1, round2

    def test_round_get_letter(self):
        round1, round2 = self.set_up_letters()
        for _ in range(50):
            self.assertNotIn(
                self.round.get_letter(),
                [round1.letter, round2.letter]
            )
    
    def test_round_save(self):
        self.assertEqual(self.round.number, 1)
        round1 = Round.objects.create(
            session=self.session
        )
        self.assertEqual(round1.number, 2)
    
    def test_session_n_rounds(self):
        self.assertEqual(self.session.n_rounds, 1)
        self.set_up_rounds()
        self.assertEqual(self.session.n_rounds, 2)
    
    def test_session_participants(self):
        self.set_up_rounds()
        user2 = self.session\
                    .round_set\
                    .get(number=2)\
                    .play_set\
                    .get(pk=2).user
        self.assertSetEqual(
            self.session.participants,
            set([self.user, user2])
        )
    
    def test_get_winner_score(self):
        play1, play2 = self.set_up_scores()
        self.assertDictEqual(
            self.session.get_winner_score,
            {play2.user.username: 5}
        )
    
    def test_session_default_categories(self):
        session = Session.objects.create(
            name='test 2',
        )
        self.assertSetEqual(
            session.categories.all(),
            Category.objects.filter(default=True)
        )

    def test_play_get_categories(self):
        session = Session.objects.create(
            name='test 2',
            random_categories=True,
        )
        round_ = Round.objects.create(session=session,)
        play = Play.objects.create(
            round=round_,
            user=self.user,
        )
        self.assertSetEqual(
            self.play.get_categories(),
            self.session.categories.all()
        )
        self.assertNotEqual(
            play.get_categories(),
            session.categories.all()
        )
    
    def test_create_playcategories(self):
        session = Session.objects.create(name='test 2')
        round_ = Round.objects.create(session=session,)
        play = Play.objects.create(
            round=round_,
            user=self.user,
        )
        categories = session.categories.values_list('name', flat=True)

        self.assertCountEqual(
            [play.category.name for play in play.categories.all()],
            list(categories),

        )

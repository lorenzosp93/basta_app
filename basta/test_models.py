"Module to test the basta app models"
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.validators import ValidationError
from django.utils.crypto import get_random_string
from unittest import mock
from copy import copy
from .models import Play, Round, Session

# Write your tests here

class TestBastaModels(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser1",
            password="testpass1",
        )
        self.session = Session.objects.create()
        self.round = Round.objects.create(
            session=self.session,
        )
        self.play = Play.objects.create(
            cur_round=self.round,
            user=self.user,
        )
    
    def test_session_create(self):
        self.assertIsInstance(self.session, Session)
    
    def test_round_create(self):
        self.assertIsInstance(self.round, Round)
        
    def test_play_create(self):
        self.assertIsInstance(self.play, Play)
    
    def test_play_validate(self):
        play = copy(self.play)
        letter = play.cur_round.letter
        play.name = letter + 'test'
        play.clean()
        next_letter = chr(ord(letter) + 1)
        wr_name = next_letter + 'test'
        play.name = wr_name
        self.assertRaises(
            ValidationError,
            play.clean)
    
    
    def set_up_plays(self, round_=None):
        if not round_:
            round_ = self.round
        play1 = copy(self.play)
        user2 = User.objects.create(
            username=get_random_string(length=8),
            password='testpass2'
        )
        play2 = Play.objects.create(
            cur_round=round_,
            user=user2,
        )
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
    
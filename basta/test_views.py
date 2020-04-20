from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from unittest import mock
from copy import copy
from .models import Play, Round, Session
from .views import (
    PlayView, RoundView, SessionView,
    play_create, play_score,
    round_create,
    session_close, session_create,
)

class TestFBViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username="testuser1",
            password="testpass1"
        )
        self.session = Session.objects.create(
            name='test 0',
        )
        self.round = Round.objects.create(
            session=self.session,
        )
        self.play = Play.objects.create(
            cur_round=self.round,
            user=self.user,
        )

    def test_session_create(self):
        s_name = 'test 1'
        request = self.factory.post(
            reverse(
                'basta:sessioncreate'
            ),
            data={
                'session_name': s_name,
            }
        )
        request.user = self.user
        response = session_create(request)
        self.assertEqual(
            response.status_code, 302
        )
        self.assertIsInstance(
            Session.objects.get(name=s_name),
            Session
        )
        self.assertEqual(
            response.url,
            reverse(
                'basta:session',
                kwargs={
                    'slug':'test-1'
                }
            )
        )
    
    def test_session_close(self):
        slug = self.session.slug
        request = self.factory.get(
            reverse(
                'basta:sessionclose',
                args=[slug]
            )
        )
        request.user = self.user
        response = session_close(request, slug)
        session = Session.objects.get(slug=slug)
        self.assertFalse(session.active)
        self.assertFalse(session.round_set.first().active)
        self.assertEqual(response.status_code, 302)

    def test_round_create(self):
        slug = self.session.slug
        self.round.active=False
        self.round.save()
        request = self.factory.get(
            reverse(
                'basta:roundcreate',
                args=[slug]
            )
        )
        request.user = self.user
        response = round_create(request, slug)
        round_ = Round.objects.get(
            session=self.session,
            number=2,
        )
        self.assertEqual(
            response.status_code, 302
        )
        self.assertIsInstance(
            round_,
            Round,
        )
        self.assertURLEqual(
            response.url,
            reverse(
                'basta:round',
                kwargs={
                    'slug':slug,
                    'number':2,
                }
            )
        )
        response2 = round_create(request, slug)
        self.assertURLEqual(
            response2.url,
            reverse(
                'basta:session',
                kwargs={
                    'slug':slug
                }
            )
        )
    
    def test_play_score(self):
        slug = self.session.slug
        number = self.round.number
        request = self.factory.post(
            reverse(
                'basta:playscore',
                args=[slug, number]
            ),
            data={
                'score': '5'
            }
        )
        request.user = self.user
        response = play_score(request, slug, number)
        play = Play.objects.get(
            user=self.user,
            cur_round=self.round,
        )
        self.assertEqual(
            play.score,
            5,
        )
        self.assertEqual(
            response.status_code, 302
        )
    
    def test_play_create(self):
        slug = self.session.slug
        number = self.round.number
        request = self.factory.get(
            reverse(
                'basta:playcreate',
                args=[slug, number]
            )
        )
        request.user = self.user
        response = play_create(request, slug, number)
        self.assertURLEqual(
            reverse('basta:round', args=[slug, number]),
            response.url
        )
        user2 = User.objects.create(
            username='testuser2',
            password='testpass2'
        )
        request.user = user2
        response2 = play_create(request, slug, number)
        play = Play.objects.get(
            user=user2,
            cur_round=self.round,
        )
        self.assertIsInstance(
            play,
            Play
        )
        self.assertEqual(
            response2.status_code, 302
        )

class TestCBViews(TestCase):
    def setUp(self):
        super(TestFBViews, self).setUp()
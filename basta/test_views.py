from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from django.http import JsonResponse
from unittest import mock
from copy import copy
from .models import Play, Round, Session
from .views import (
    PlayView, RoundView, SessionView,
    play_create, play_score,
    round_create,
    session_close, session_create,
)
from .forms import PlayForm

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
            round=self.round,
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
            round=self.round,
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
            round=self.round,
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
            round=self.round,
            user=self.user,
        )

    @staticmethod
    def setup_view(view, request, *args, **kwargs):
        """
        Mimic ``as_view()``, but returns view instance.
        Use this function to get view instances on which you can run unit tests,
        by testing specific methods.
        """

        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    def set_up_round_view(self, slug=None, number=None, user=None):
        if not slug:
            slug = self.session.slug
        if not number:
            number = self.round.number
        request = self.factory.get(
            reverse(
                'basta:round',
                args=[slug,number]
            )
        )
        if not user:
            request.user = self.user
        return self.setup_view(
            RoundView(),
            request,
            slug=slug,
            number=number,
        ), request


    def test_round_get_user_play(self):
        view, _ = self.set_up_round_view()
        user = User.objects.create(
            username='username2',
            password='password2'
        )
        play = Play.objects.create(
            round=self.round,
            user=user
        )
        view.object = self.round
        context = view.get_context_data(
            user=user,
        )
        self.assertEqual(
            context.get('my_play'),
            play
        )

    def test_round_get_object(self):
        round_ = Round.objects.create(
            session=self.session
        )
        view, _ = self.set_up_round_view(
            slug=self.session.slug,
            number=round_.number,
        )
        self.assertEqual(
            view.get_object(),
            round_,
        )
    
    def test_round_get(self):
        view, request = self.set_up_round_view()
        response = view.get(request)
        self.assertEqual(
            response.status_code, 200
        )
    
    def set_up_play_view(self, request=None, slug=None, number=None, user=None):
        if not slug:
            slug = self.session.slug
        if not number:
            number = self.round.number
        if not request:    
            request = self.factory.post(
            reverse(
                'basta:round',
                args=[slug,number]
            )
        )
        if not user:
            request.user = self.user
        return self.setup_view(
            PlayView(),
            request,
            slug=slug,
            number=number,
        ), request

    def set_up_formdata(self):
        l = self.round.letter
        return {
            "name": l + "name",
            "brand": l + "brand"
        }
    
    def set_up_form(self, data=None, play=None):
        if not data:
            data = self.set_up_formdata()
        form = PlayForm(data)
        if not play:
            form.instance = self.play
        return form

    def test_play_get_success_url(self):
        view, _ = self.set_up_play_view()
        form = self.set_up_form()
        url = view.get_success_url(form)
        self.assertURLEqual(
            url,
            reverse(
                'basta:round',
                args=[
                    self.session.slug,
                    self.round.number,
                ]
            )
        )
    
    def test_play_finish_round(self):
        view, request = self.set_up_play_view()
        form = self.set_up_form()
        response = view.finish_round(form)
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(
            response.url,
            view.get_success_url(form)
        )
    
    def test_play_ajax_finish_round(self):
        request = self.factory.post(
            reverse(
                'basta:play',
                args=[
                    self.session.slug,
                    self.round.number,
                ]
            ),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        view, _ = self.set_up_play_view(request)
        form = self.set_up_form()
        response = view.finish_round(form)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response,
            JsonResponse
        )
    
    def test_play_upon_valid_stop(self):
        view, _ = self.set_up_play_view()
        form = self.set_up_form()
        response = view.upon_valid_stop(form)
        self.assertURLEqual(
            response.url,
            view.finish_round(form).url
        )
        self.assertFalse(self.round.active)

    def test_form_logic(self):
        view, request = self.set_up_play_view()
        request.POST = {"Stop": True}
        form = self.set_up_form()
        response = view.form_logic(request, form)
        self.assertEqual(response.status_code, 302)
    
    def test_form_logic_stop(self):
        view, request = self.set_up_play_view()
        form = self.set_up_form()
        response = view.form_logic(request, form)
        self.assertURLEqual(
            response.url,
            view.upon_valid_stop(form).url,
        )

    def test_form_logic_inactive(self):
        view, request = self.set_up_play_view()
        form = self.set_up_form()
        form.instance.round.active = False
        response = view.form_logic(request, form)
        self.assertURLEqual(
            response.url,
            view.get_success_url(form),
        )

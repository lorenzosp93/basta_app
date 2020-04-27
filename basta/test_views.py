from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from django.http import JsonResponse
from unittest import mock
from copy import copy
from .models import Play, Round, Session, PlayCategory, Category
from .views import (
    PlayView, RoundView, SessionView,
    play_create, play_score,
    round_create,
    session_close, session_create,
)
from .forms import PlayCategoryFormSet, PlayForm

class TestFBViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser1")
        self.category = Category.objects.get(
            name='name',
            default=True
        )
        self.session = Session.objects.create(
            name='test 0',
        )
        self.session.categories.set([self.category])
        self.round = Round.objects.create(
            session=self.session,
        )
        self.play = Play.objects.create(
            round=self.round,
            user=self.user,
        )
        self.playcategory = PlayCategory(
            play=self.play,
            category=self.category,
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
        session = Session.objects.get(name=s_name)
        self.assertEqual(
            response.status_code, 302
        )
        self.assertIsInstance(
            session,
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
        self.assertEqual(
            self.user,
            session.created_by
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
        self.assertEqual(session.modified_by, self.user)

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
        self.assertEqual(
            round_.created_by,
            self.user
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
        # test redirect to play since play already exists for user
        self.assertURLEqual(
            reverse('basta:play', args=[slug, number]),
            response.url
        )
        user2 = User.objects.create_user(username='testuser2')
        request.user = user2
        response2 = play_create(request, slug, number)
        play = Play.objects.get(
            user=user2,
            round=self.round,
        )
        # test play creation
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
        self.user = User.objects.create_user(username="testuser1")
        self.category = Category.objects.get(
            name='name'
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
        self.playcategory = PlayCategory.objects.create(
            play=self.play,
            category=self.category,
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
        user = User.objects.create_user(username='username2')
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
            "categories-0-id": self.playcategory.id,
            "categories-0-play": self.play.id,
            "categories-0-value": l + "name",
            "categories-TOTAL_FORMS": 1,
            "categories-INITIAL_FORMS": 1,
            "categories-MIN_NUM_FORMS": 0,
            "categories-MAX_NUM_FORMS": 1000,
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
        view.object = self.play
        view.request.POST = self.set_up_formdata()
        url = view.get_success_url()
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
        view.object = self.play   
        view.request.POST = self.set_up_formdata()     
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
        view.object = self.play
        view.request.POST = self.set_up_formdata()
        response = view.finish_round(form)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response,
            JsonResponse
        )
    
    def test_play_upon_valid_stop(self):
        view, _ = self.set_up_play_view()
        form = self.set_up_form()
        view.object = self.play
        view.request.POST = self.set_up_formdata()
        response = view.upon_valid_stop(form, self.user)
        self.assertURLEqual(
            response.url,
            view.finish_round(form).url
        )
        self.assertFalse(self.round.active)
        self.assertEqual(
            self.round.modified_by,
            self.user
        )

    def test_form_logic(self):
        view, _ = self.set_up_play_view()
        view.request.POST = self.set_up_formdata()
        view.request.POST.update({"Stop": True})
        form = self.set_up_form()
        view.object = self.play
        response = view.form_logic(form)
        self.assertEqual(response.status_code, 302)

    def test_form_logic_inactive(self):
        view, _ = self.set_up_play_view()
        form = self.set_up_form()
        form.instance.round.active = False
        view.request.POST = self.set_up_formdata()
        view.object = self.play
        response = view.form_logic(form)
        self.assertURLEqual(
            response.url,
            view.get_success_url(form),
        )

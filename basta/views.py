from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, UpdateView
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from random import randint
import json
from .base.views import AjaxableResponseMixin
from .forms import PlayForm
from .models import Round, Session, Play

# Create your views here.

class PlayView(AjaxableResponseMixin, UpdateView):
    template_name = "basta/play.html"
    form_class = PlayForm

    def get_object(self):
        session = Session.objects.get(slug=self.kwargs.get('slug'))
        round_ = Round.objects.get(session=session, number=self.kwargs.get('number'))
        return round_.play_set.get(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        return self.form_logic(request, form)

    def form_logic(self, request, form):
        "Defines the logic of what to do when a POST request is received"
        if form.instance.round.active:
            if form.is_valid():
                if request.POST.get("Stop"):
                    return self.upon_valid_stop(form, request.user)
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.finish_round(form)
    
    def upon_valid_stop(self, form, user):
        "Trigger for when player hits the Stop button"
        object_deactivate(form.instance.round, user)
        return self.finish_round(form)

    def finish_round(self, form):
        if self.request.is_ajax():
            return JsonResponse({"stop":True}, status=200)
        return redirect(self.get_success_url(form))

    def get_success_url(self, form=None):
        if not form:
            form = self.get_form()
        round_ = form.instance.round
        return reverse("basta:round", kwargs={
            "slug":round_.session.slug,
            "number":round_.number,
        })

def object_deactivate(obj, user):
    obj.active = False
    return obj.save(user=user)

class RoundView(AjaxableResponseMixin, DetailView):
    template_name = "basta/round.html"
    model = Round
    context_object_name = "round"

    def get_object(self):
        session = Session.objects.get(slug=self.kwargs.get('slug'))
        return Round.objects.get(session=session, number=self.kwargs.get('number'))

    def get_context_data(self, **kwargs):
        user = kwargs.pop('user')
        context = super().get_context_data(**kwargs)
        try:    
            user_play = user.play_set.get(round=self.object)
        except:
            user_play = None
        context.update({'my_play': user_play})
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        context = self.get_context_data(object=self.object, user=user)
        return self.render_to_response(context)

class SessionView(DetailView):
    template_name = "basta/session.html"
    model = Session
    context_object_name = "session"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'active_round': self.object.round_set.filter(active=True),
        })
        return context

def poll_session_refresh_view(request, slug):
    if request.is_ajax():
        if Session.objects\
                  .get(slug=slug)\
                  .round_set\
                  .filter(active=True):
            return JsonResponse({}, status=200)
        else:
            return JsonResponse({}, status=404)

class SessionListView(ListView):
    template_name = "basta/start.html"
    model = Session
    context_object_name = "sessions"
    paginate_by = 5
    ordering = ['-created_at']

def redirect_play(slug, number):
    return redirect(reverse("basta:play", kwargs={
        'slug':slug,
        'number':number,
    }))

def redirect_round(slug, number):
    return redirect(
        reverse('basta:round', kwargs={'slug':slug, 'number':number})    
    )

def redirect_session(slug):
    return redirect(reverse('basta:session', args=[slug]))

@login_required
def play_create(request, slug, number):
    session = Session.objects.get(slug=slug)
    round_ = Round.objects.get(number=number, session=session)
    user = request.user
    this_play = round_.play_set.filter(user=user)
    if user and not this_play and round_.active:
        new_play = Play.objects.create(
            round=round_,
            user=user
        )
        return redirect_play(slug, number)
    elif round_.active:
        return redirect_play(slug, number)
    else:
        return redirect_round(slug, number)

@login_required
def play_score(request, slug, number):
    session = Session.objects.get(slug=slug)
    round_ = Round.objects.get(number=number, session=session)
    user = request.user
    play = Play.objects.get(
        round=round_,
        user=user,
    )
    if not play.score > 0:
        score = request.POST.get('score', '0')
        play.score = int(score)
        play.save(update_fields=["score"])
    return redirect_round(slug, number)

@login_required
def round_create(request, slug):
    session = Session.objects.get(slug=slug)
    if not session.round_set.filter(active=True) and session.active:
        new_round = Round.objects.create(
            session=session,
            created_by=request.user,
            modified_by=request.user,
        )
        return redirect_round(slug, new_round.number)
    else:
        return redirect_session(slug)

@login_required
def session_create(request):
    name = request.POST.get('session_name', '')
    new_session = Session.objects.create(
        name=name,
        created_by=request.user,
        modified_by=request.user,
    )
    return redirect_session(new_session.slug)

@login_required
def session_close(request, slug):
    session = Session.objects.get(slug=slug)
    object_deactivate(session, request.user)
    for round_ in session.round_set.all():
        object_deactivate(round_, request.user)
    return redirect(reverse("basta:home"))


from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, UpdateView
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from random import randint
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        return self.form_logic(request, form)

    def form_logic(self, request, form):
        "Defines the logic of what to do when a POST request is received"
        if form.instance.cur_round.active:
            if form.is_valid():
                if request.POST.get("Stop"):
                    return self.upon_valid_stop(form)
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.finish_round(form)
    


    def upon_valid_stop(self, form):
        "Trigger for when player hits the Stop button"
        round_ = form.instance.cur_round
        round_.active = False
        round_.save()
        return self.finish_round(form)

    def finish_round(self, form):
        return redirect(self.get_success_url(form))

    def get_success_url(self, form=None):
        if not form:
            form = self.get_form()
        round_ = form.instance.cur_round
        return reverse("basta:round", kwargs={
            "slug":round_.session.slug,
            "number":round_.number,
        })

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
            user_play = user.play_set.get(cur_round=self.object)
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

class SessionListView(ListView):
    template_name = "basta/start.html"
    model = Session
    context_object_name = "sessions"

def play_create(request, slug, number):
    session = Session.objects.get(slug=slug)
    round_ = Round.objects.get(number=number, session=session)
    user = request.user
    if user and not round_.play_set.filter(user=user):
        new_play = Play.objects.create(
            cur_round=round_,
            user=user
        )
        return redirect(reverse("basta:play", kwargs={
            'slug':slug,
            'number':number,
        }))
    else:
        return redirect(
                reverse('basta:round', kwargs={'slug':slug, 'number':number}), 
                context={'error': _('User is not authenticated')}
            )

def play_score(request, slug, number):
    session = Session.objects.get(slug=slug)
    round_ = Round.objects.get(number=number, session=session)
    user = request.user
    play = Play.objects.get(
        cur_round=round_,
        user=user,
    )
    if not play.score > 0:
        score = request.POST.get('score', '0')
        play.score = int(score)
        play.save(update_fields=["score"])
    return redirect(
        reverse('basta:round', kwargs={'slug':slug, 'number':number})
    )

def round_create(request, slug):
    session = Session.objects.get(slug=slug)
    letter = chr(65 + randint(0,25))
    if not letter in session.round_set.values() and not session.round_set.filter(active=True):
        new_round = Round.objects.create(
            letter = letter,
            session=session,
        )
        return redirect(reverse("basta:round", kwargs={
            'slug':slug,
            'number':new_round.number
        }))
    else:
        return redirect(
                reverse('basta:session', kwargs={'slug':slug}), 
                context={'error': _('Letter %(letter)s' % {'letter': letter})}
            )

def session_create(request):
    name = request.POST.get('session_name', '')
    new_session = Session.objects.create(
        name=name,
    )
    return redirect(reverse("basta:session", kwargs={'slug':new_session.slug}))

def session_close(request, slug):
    session = Session.objects.get(slug=slug)
    session.active = False
    session.save()
    return redirect(reverse("basta:home"))

from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, UpdateView
from .base.views import AjaxableResponseMixin
from .forms import PlayForm
from .models import Round, Session

# Create your views here.
class PlayView(AjaxableResponseMixin, UpdateView):
    template_name = "basta/play.html"
    form_class = PlayForm
    # success_url = reverse('basta:round', kwargs={
    #     'session': lambda self: self.get_form().instance.cur_round.session.pk,
    #     'round': lambda self: self.get_form().instance.cur_round.pk,
    # })
    def get_object(self):
        session = Session.objects.get(slug=self.kwargs.get('slug'))
        round_ = Round.objects.get(session=session, number=self.kwargs.get('number'))
        return round_.play_set.get(user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        self.form_logic(request, form)

    def form_logic(self, request, form):
        "Defines the logic of what to do when a POST request is received"
        if form.instance.cur_round.active:
            if form.is_valid():
                if request.get("Stop"):
                    upon_valid_stop(form)
                form.save()
            else:
                self.form_invalid(self, form)
        else:
            self.finish_round()

    def upon_valid_stop(self, form):
        "Trigger for when player hits the Stop button"
        form.instance.cur_round.active = False
        return self.finish_round()

    def finish_round(self):
        return redirect(self.get_success_url())

class RoundView(AjaxableResponseMixin, DetailView):
    template_name = "basta/round.html"
    model = Round
    context_object_name = "rounds"

    def get_object(self):
        session = Session.objects.get(slug=self.kwargs.get('slug'))
        return Round.objects.get(session=session, number=self.kwargs.get('number'))
    
class SessionView(DetailView):
    template_name = "basta/session.html"
    model = Session
    context_object_name = "session"

class SessionListView(ListView):
    template_name = "basta/start.html"
    model = Session
    context_object_name = "sessions"

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
from django.shortcuts import render
from django.views.generic import FormView
from .forms import PlayForm

# Create your views here.

class PlayView(FormView):
    template_name = "basta/play.html"
    form_class = PlayForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

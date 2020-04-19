from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import CreateView
from .forms import PlayForm

# Create your views here.
class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

class PlayView(AjaxableResponseMixin, CreateView):
    template_name = "basta/play.html"
    form_class = PlayForm
    success_url = "basta/round.html"
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if request.get("Basta"):
            pass
        
        if form.is_valid():
            self.form_valid(self, form)
        else:
            self.form_invalid(self, form)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

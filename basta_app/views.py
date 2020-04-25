from django.views.generic import CreateView, edit
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from .forms import MyUserCreationForm

class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = MyUserCreationForm

    def get_success_url(self):
        return reverse('basta:home')

    def form_valid(self, form, request):
        self.object = form.save()
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        auth_user = authenticate(username=username, password = raw_password)
        login(request, auth_user)
        return redirect(self.get_success_url())
    

    def post(self, request):
        self.object=None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form)

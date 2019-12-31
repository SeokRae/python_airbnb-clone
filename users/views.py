from django.shortcuts import render, redirect, reverse

# http://ccbv.co.uk/projects/Django/2.2/django.views.generic.edit/FormView
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from . import forms

# Create your views here.


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    initial = {"email": "kslbsh@gmail.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)

        return super().form_valid(form)


# https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.forms.AuthenticationForm
def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))

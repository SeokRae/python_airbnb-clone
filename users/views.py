from django.shortcuts import render, redirect, reverse

# http://ccbv.co.uk/projects/Django/2.2/django.views.generic.edit/FormView
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from . import forms, models

# github login
import os

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


class SignUpView(FormView):
    # TypeError 발생 시 html 확인
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    initial = {
        "first_name": "SeokRae",
        "last_name": "Kim",
        "email": "kslbsh@gmail.com",
    }

    def form_valid(self, form):
        form.save()

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)

        user.verify_email()
        return super().form_valid(form)


def complete_varification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        # user.email_secret = ""
        user.save()
        # TODO add Success Message
    except models.User.DoesNotExist:
        # TODO Error Message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GITHUB_CLIENT_ID")
    redirect_uri = "http://localhost:8000/users/login/github/callback"
    auth_url = "https://github.com/login/oauth/authorize"
    url = (
        f"{auth_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )
    return redirect(url)


def github_callback(request):
    pass

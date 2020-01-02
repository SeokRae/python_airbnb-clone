from django.shortcuts import redirect, reverse

# http://ccbv.co.uk/projects/Django/2.2/django.views.generic.edit/FormView
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from . import forms, models

# github login
import os
import requests

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


# https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/
def github_login(request):
    client_id = os.environ.get("GITHUB_CLIENT_ID")
    auth_url = "https://github.com/login/oauth/authorize"
    redirect_uri = "http://localhost:8000/users/login/github/callback"
    url = (
        f"{auth_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )
    return redirect(url)


class GitHubException(Exception):
    pass


# user Accept 될 때 웹사이트 로그인
def github_callback(request):
    try:
        code = request.GET.get("code", None)

        client_id = os.environ.get("GITHUB_CLIENT_ID")
        client_secret = os.environ.get("GITHUB_CLIENT_SECRET")
        access_url = "https://github.com/login/oauth/access_token"

        if code is not None:
            token_request = requests.post(
                f"{access_url}?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            # github token error
            if error is not None:
                raise GitHubException()
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                # user profile
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                # profile 정상적으로 가져올 경우
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")

                    try:
                        # aready user exist
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GitHubException()

                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=email,
                            email=email,
                            first_name=name,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        # https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#django.contrib.auth.models.User.set_unusable_password
                        user.set_unusable_password()
                        user.save()

                    # 사용자가 이미 있으면 login, 없으면 만들고 로그인
                    login(request, user)

                    return redirect(reverse("core:home"))

                else:
                    raise GitHubException()
        else:
            raise GitHubException()

    except GitHubException:  # 예외 발생시 redirect
        return redirect(reverse("users:login"))


# Kakao Login
def kakao_login(request):
    kakao_oauth_url = "https://kauth.kakao.com/oauth/authorize"
    app_key = os.environ.get("KAKAO_CLIENT_ID")
    redirect_uri = "http://localhost:8000/users/login/kakao/callback"
    return redirect(
        f"{kakao_oauth_url}?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        pass
    except KakaoException:
        return redirect(reverse("core:home"))
    pass

from django.shortcuts import redirect, reverse

# http://ccbv.co.uk/projects/Django/2.2/django.views.generic.edit/FormView
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from . import forms, models

# github login
import os
import requests

# image
from django.core.files.base import ContentFile

# messages
from django.contrib import messages

# Create your views here.


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)

        return super().form_valid(form)


# https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.forms.AuthenticationForm
def log_out(request):
    messages.info(request, f"See you later")
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
                raise GitHubException("Can't get access token")
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
                            raise GitHubException(
                                f"Please log in with: {user.login_method}"
                            )

                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=email,
                            email=email,
                            first_name=name,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        # https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#django.contrib.auth.models.User.set_unusable_password
                        user.set_unusable_password()
                        user.save()

                    # 사용자가 이미 있으면 login, 없으면 만들고 로그인
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))

                else:
                    raise GitHubException("Can't get your profile")
        else:
            raise GitHubException("Can't get code")

    except GitHubException as e:  # 예외 발생시 redirect
        messages.error(request, e)
        return redirect(reverse("users:login"))


# Kakao Login
def kakao_login(request):
    kakao_oauth_url = "https://kauth.kakao.com/oauth/authorize"
    client_id = os.environ.get("KAKAO_CLIENT_ID")
    redirect_uri = "http://localhost:8000/users/login/kakao/callback"
    # kakao API redirect_url
    return redirect(
        f"{kakao_oauth_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


# kakao Exception
class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_CLIENT_ID")
        redirect_uri = "http://localhost:8000/users/login/kakao/callback"
        token_url = "https://kauth.kakao.com/oauth/token"
        token_request = requests.get(
            f"{token_url}?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)

        # kakao error check
        if error is not None:
            raise KakaoException("Can't get authorization code")
        # https://developers.kakao.com/docs/restapi/user-management#%EC%82%AC%EC%9A%A9%EC%9E%90-%EC%A0%95%EB%B3%B4-%EC%9A%94%EC%B2%AD
        access_token = token_json.get("access_token")
        profile_domain = "https://kapi.kakao.com"
        profile_uri = "/v2/user/me"

        profile_request = requests.get(
            f"{profile_domain}/{profile_uri}",
            headers={f"Authorization": f"Bearer {access_token}"},
        )

        profile_json = profile_request.json()

        profile_account = profile_json.get("kakao_account", None)
        email = profile_account.get("email", None)

        # email None check
        if email is None:
            raise KakaoException("Please also give me your email")

        profile = profile_account.get("profile")

        # properties
        nickname = profile.get("nickname")
        profile_image = profile.get("profile_image_url")

        # user check
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please login with: {user.login_method}")

        except models.User.DoesNotExist:  # user 없으면 만들기

            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()

            # profile image
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )

        messages.success(request, f"Welcome back {user.first_name}")
        login(request, user)
        return redirect(reverse("core:home"))

    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(UpdateView):

    model = models.User
    template_name = "users/update_profile.html"
    fields = (
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthday",
        "language",
        "currency",
    )

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["birthday"].widget.attrs = {"placeholder": "birthday"}
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        return form


class UpdatePasswordView(PasswordChangeView):

    template_name = "users/update_password.html"

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }
        return form

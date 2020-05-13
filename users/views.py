import os
import requests
from django.http import HttpResponse
from django.utils import translation

# Create your views here.
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models, mixins

# kakao avatar File 읽기
from django.core.files.base import ContentFile

# messages
from django.contrib import messages

# profile Success
from django.contrib.messages.views import SuccessMessageMixin

# auth
from django.contrib.auth.decorators import login_required


# class-based view
# View -> FormView로 변경 시, get post 함수 차이
class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm

    # FIXME 테스트용 default 값 설정
    initial = {"email": "test@gmail.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        # 인증 함수
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            # 로그인 함수
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, f"See you later")
    # 로그아웃 함수
    logout(request)
    return redirect(reverse("core:home"))


# class-based view
class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    initial = {
        "first_name": "test_first",
        "last_name": "test_last",
        "email": "test@gmail.com",
    }

    # request에서 넘어온 form 값에 대한 validation check 후에 user 등록, 로그인
    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            user.verify_email()
            return redirect(reverse("core:home"))


# email verify
def complete_verification(request, key):

    try:
        # todo add success message
        user = models.User.objects.get(email_secret=key)

        # 이메일 인증시 user의 email_secret 값을 제거
        user.email_verified = True
        user.email_secret = ""

        # email_verified
        user.save()

    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


# Github 예외처리
class GithubException(Exception):
    pass


# GitHub Login
# 1. Users are redirected to request their GitHub identity
# 2. Users are redirected back to your site by GitHub
# 3. Your app accesses the API with the user's access token
def github_login(request):
    # https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://localhost:8000/users/login/github/callback"
    # 1. Request a user's GitHub identity
    request_url = f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    return redirect(request_url)


# GitHub callback
def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)  # request.GET code 값으로 access_token 요청

        if code is not None:
            # 2. Users are reirected back to your site by GitHub
            token_url = f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}"
            token_request = requests.post(
                token_url, headers={"Accept": "application/json"},
            )
            # access_token 확인
            token_json = token_request.json()
            error = token_json.get("error", None)

            if error is not None:
                raise GithubException("Can't get access token")
            else:
                access_token = token_json.get("access_token")
                # 3. Use the Access token to access the API
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)  # duplicate check user pk
                if username is not None:  # username 있는 경우 login
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    avatar = profile_json.get("avatar_url")

                    try:  # user get에 대한 예외처리
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        # Username이 있고 user 없는 경우? user 생성
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()

                        if avatar is not None:
                            photo_request = requests.get(avatar)
                            # user를 따로 save할 필요 없음
                            user.avatar.save(
                                # username이 한글일 수도 있으니 email의 로컬파트를 사용
                                f"{name}-avatar",
                                ContentFile(photo_request.content),
                            )

                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:  # username Exception
                    raise GithubException("Can't get your profile")

        else:  # code Exception
            raise GithubException("Can't get code")
    except GithubException as e:  # send error message
        messages.error(request, e)
        return redirect(reverse("users:login"))


class KakaoException(Exception):
    pass


# kakao login function
def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://localhost:8000/users/login/kakao/callback"
    request_identiy = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(request_identiy)


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://localhost:8000/users/login/kakao/callback"
        access_token_url = f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"

        # access_token 요청
        token_request = requests.get(access_token_url)
        token_json = token_request.json()

        # error 처리
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code.")

        access_token = token_json.get("access_token")
        kakao_user_info_url = "https://kapi.kakao.com/v2/user/me"
        # request profile
        profile_request = requests.get(
            kakao_user_info_url, headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account", None)
        kakao_profile = kakao_account.get("profile", None)
        # email verified check
        has_email = kakao_account.get("has_email", None)

        if has_email is False:
            raise KakaoException("Please also give me your email")

        # user 생성시 필요한 값
        kakao_email = kakao_account.get("email", None)
        kakao_username = kakao_email.split("@")[0]
        kakao_thumbnail = kakao_profile.get("thumbnail_image_url", None)

        try:
            user = models.User.objects.get(email=kakao_email)
            if user.login_method != models.User.LOGING_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")

        except models.User.DoesNotExist:
            # email이 없는 경우 user 생성
            user = models.User.objects.create(
                email=kakao_email,
                username=kakao_email,
                first_name=kakao_username,
                login_method=models.User.LOGING_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if kakao_thumbnail is not None:
                photo_request = requests.get(kakao_thumbnail)
                # user를 따로 save할 필요 없음
                user.avatar.save(
                    # username이 한글일 수도 있으니 email의 로컬파트를 사용
                    f"{kakao_username}-avatar",
                    ContentFile(photo_request.content),
                )

        messages.success(request, f"Welcome back {user.first_name}")

        # user login 처리
        login(request, user)
        return redirect(reverse("core:home"))

    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


# User Profile
class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"


# User Update Profile
class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.User
    template_name = "users/user_profile.html"
    fields = (
        "first_name",
        "last_name",
        "gender",
        "bio",
        "avatar",
        "birthdate",
        "language",
        "currency",
    )

    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        form.fields["bio"].widget.attrs = {"placeholder": "Bio"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "years-month-day"}
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        return form


# password change view
class UpdatePasswordView(
    mixins.EmailLoginOnlyView,
    mixins.LoggedInOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):

    template_name = "users/user_password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }
        return form

    # redirect
    def get_success_url(self):
        return self.request.user.get_absolute_url()


# 호스팅 관리
@login_required
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))


# language translate
def switch_language(request):
    lang = request.GET.get("lang", None)
    if lang is not None:
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return HttpResponse(status=200)

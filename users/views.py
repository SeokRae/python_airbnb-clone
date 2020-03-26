import os
import requests

# Create your views here.
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models


# class-based view
# View -> FormView로 변경 시, get post 함수 차이
class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    # FIXME 테스트용 default 값 설정
    initial = {"email": "seok@gmail.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        # 인증 함수
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            # 로그인 함수
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    # 로그아웃 함수
    logout(request)
    return redirect(reverse("core:home"))


# class-based view
class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    initial = {
        "first_name": "test_first",
        "last_name": "test_last",
        "email": "seok.ref@gmail.com",
    }

    # request에서 넘어온 form 값에 대한 validation check 후에 user 등록, 로그인
    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


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
                raise GithubException()
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

                    try:  # user get에 대한 예외처리
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException()
                    except models.User.DoesNotExist:
                        # Username이 있고 user 없는 경우? user 생성
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        user.save()

                    login(request, user)
                    return redirect(reverse("core:home"))
                else:  # username Exception
                    raise GithubException()
        else:  # code Exception
            raise GithubException()
    except GithubException:  # send error message
        return redirect(reverse("users:login"))

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


# GitHub Login
# 1. Users are redirected to request their GitHub identity
# 2. Users are redirected back to your site by GitHub
# 3. Your app accesses the API with the user's access token
def github_login(request):
    # https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://localhost:8000/users/login/github/callback"
    request_url = f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    return redirect(request_url)


# GitHub callback
def github_callback(request):
    client_id = os.environ.get("GH_ID")
    client_secret = os.environ.get("GH_SECRET")
    code = request.GET.get("code", None)
    if code is not None:
        callback_url = f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}"
        request = requests.post(callback_url, headers={"Accept": "application/json"},)
        # request 확인
        print(request.json())
    else:
        return redirect(reverse("core:home"))

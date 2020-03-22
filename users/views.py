# Create your views here.
from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


# class-based view
class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={"email": "seok@gmail.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            # 사용자 인증 함수
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # 로그인 함수
                login(request, user)
                return redirect(reverse("core:home"))

        return render(request, "users/login.html", {"form": form})


def log_out(request):
    # 로그아웃 함수
    logout(request)
    return redirect(reverse("core:home"))

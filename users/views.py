# Create your views here.
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


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


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    initial = {
        "first_name": "SeokRae",
        "last_name": "Kim",
        "email": "seokr@gmail.com",
    }

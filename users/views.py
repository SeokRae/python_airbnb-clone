# Create your views here.
from django.views import View
from django.shortcuts import render
from . import forms


# class-based view
class LoginView(View):

    # 기본 함수
    def get(self, request):
        form = forms.LoginForm(initial={"email": "seok@gmail.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        return render(request, "users/login.html", {"form": form})

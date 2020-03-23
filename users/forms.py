from django import forms
from . import models


# 로그인 Form
class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # email & password validation check
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))

        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


# 회원가입 Form
class SignUpForm(forms.Form):
    # Form Input
    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    # widget 수정으로 CharField에서 PasswordInput으로 수정
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # user duplicate check
    def clean_email(self):
        email = self.cleaned_data.get("email")

        try:
            # db에 해당 user가 존재함
            users = models.User.objects.get(email=email)
            raise forms.ValidationError(f"{users} already exists with that email")
        except models.User.DoesNotExist:
            # db에 해당 user가 없는 경우
            return email

    # password 체크
    def clean_password(self):

        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

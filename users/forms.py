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
class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    # widget 수정으로 CharField에서 PasswordInput으로 수정
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # password와 password1의 diff 체크는 password1에서 이루어지면 되므로 clean_password1을 사용
    def clean_password1(self):

        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    # ModelForm의 save를 override해서 추가적으로 필요한 필드(username, password)에 대해서 작업
    def save(self, *args, **kwargs):
        # DB에는 저장하지 않고 객체만 생성
        user = super().save(commit=False)

        # 추가적인 필드 작업
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user.username = email
        # password 암호화
        user.set_password(password)
        user.save()

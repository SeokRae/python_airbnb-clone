from django import forms
from . import models


class LoginForm(forms.Form):
    """ LoginForm class Definition """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            # TODO 데이터는 Email과 username이 같아야 한다. 여기서는 임시로 email비교
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password Error"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):
    """ SignUpForm Form Definition """

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        # password same Check
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    # override
    def save(self, *args, **kwargs):
        user = super().save(commit=False)

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        # 추가적으로 등록되어야 하는 필드
        user.username = email
        user.set_password(password)
        user.save()

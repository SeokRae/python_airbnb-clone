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
            self.add_error("email", self.add_error("Email Error"))

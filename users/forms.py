from django import forms
from . import models


class LoginForm(forms.Form):
    """ LoginForm class Definition """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User Does Not Exist")

    def clean_password(self):
        print(self.cleaned_data)
        return self.cleaned_data

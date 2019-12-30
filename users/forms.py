from django import forms


class LoginForm(forms.Form):
    """ LoginForm class Definition """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

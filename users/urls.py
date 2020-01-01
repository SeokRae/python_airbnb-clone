from django.urls import path
from . import views

app_name = "users"

# management for User URL
urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("login/github", views.github_login, name="github_login"),
    path("login/github/callback", views.github_callback, name="github_callback"),
    path("logout", views.log_out, name="logout"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("verify/<str:key>", views.complete_varification, name="complete_varification"),
]

from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    # OAuth
    path("login/github/", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("login/kakao/", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback/", views.kakao_callback, name="kakao-callback"),
    # email confirm
    path(
        "verify/<str:key>/", views.complete_verification, name="complete-verification"
    ),
    # User profile
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    path("<int:pk>/profile/", views.UpdateProfileView.as_view(), name="update"),
    path(
        "<int:pk>/profile/password/",
        views.UpdatePasswordView.as_view(),
        name="password",
    ),
    path("switch-hosting/", views.switch_hosting, name="switch-hosting"),
]

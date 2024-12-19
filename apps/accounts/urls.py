from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "accounts"

urlpatterns = [
    path(
        "signup/",
        views.SignUpView.as_view(),
        name="signup",
    ),
    path(
        "login/",
        views.LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(next_page="index"),
        name="logout",
    ),
    path(
        "profile/",
        views.ProfileView.as_view(),
        name="profile",
    ),
    path(
        "profile/edit/",
        views.ProfileUpdateView.as_view(),
        name="profile_edit",
    ),
    path(
        "password/change/",
        views.PasswordChangeView.as_view(),
        name="password_change",
    ),
]

from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("activate/<uidb64>/<token>", views.ActivateView.as_view(), name="activate"),
    path(
        "verify-email/",
        views.VerifyEmailView.as_view(),
        name="verify_email",
    ),
    path(
        "change-email/",
        login_required(views.ChangeEmail.as_view(), login_url="login"),
        name="change_email",
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="frontend/authentication/reset_password/password_reset.html"
        ),
        name="password-reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name="frontend/authentication/reset_password/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="frontend/authentication/reset_password/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        PasswordResetCompleteView.as_view(
            template_name="frontend/authentication/reset_password/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

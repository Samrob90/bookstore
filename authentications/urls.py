from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("activate/<uidb64>/<token>", views.ActivateView.as_view(), name="activate"),
    path(
        "verify-email/",
        login_required(views.VerifyEmailView.as_view(), login_url="login"),
        name="verify_email",
    ),
    path(
        "change-email/",
        login_required(views.ChangeEmail.as_view(), login_url="login"),
        name="change_email",
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]

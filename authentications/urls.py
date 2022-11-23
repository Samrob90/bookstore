from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("activate/<uidb64>/<token>", views.ActivateView.as_view(), name="activate"),
]

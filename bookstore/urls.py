"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from frontend.views import account_social_sigup, account_google_callback

urlpatterns = [
    path("admin/", admin.site.urls),
    # path(
    #     "accounts/google/login/callback/",
    #     account_google_callback,
    #     name="google_account_callback_redirect",
    # ),
    path("", include("frontend.urls")),
    path(
        "accounts/social/signup/",
        account_social_sigup,
        name="account_signup_redirect",
    ),
    path("", include("authentications.urls")),
    path("accounts/", include("allauth.urls")),
    path("cpanel/", include("cpanel.urls")),
    path("account/", include("user_account.urls")),
    path("blog/", include("blog.urls")),
    # path("ratings/", include("star_ratings.urls", namespace="ratings")),
]

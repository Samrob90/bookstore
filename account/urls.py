from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings


urlpatterns = [
    path(
        "",
        login_required(views.AccountHomeView.as_view(), login_url=settings.LOGIN_URL),
        name="account",
    ),
    path(
        "orders/",
        login_required(views.OrderView.as_view(), login_url=settings.LOGIN_URL),
        name="orders",
    ),
    path(
        "downloads/",
        login_required(views.DownloadsView.as_view(), login_url=settings.LOGIN_URL),
        name="downloads",
    ),
    path(
        "addresses/",
        login_required(views.AddressesView.as_view(), login_url=settings.LOGIN_URL),
        name="addresses",
    ),
    path(
        "profile/",
        login_required(views.AccountDetails.as_view(), login_url=settings.LOGIN_URL),
        name="profile",
    ),
    path(
        "wishlist/",
        login_required(views.WishlistView.as_view(), login_url=settings.LOGIN_URL),
        name="wishlist",
    ),
]

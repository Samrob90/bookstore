from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from frontend import models as frontend_model

# Create your views here.
class AccountHomeView(TemplateView):
    template_name: str = "frontend/account/dashboard.html"


class OrderView(TemplateView):
    template_name: str = "frontend/account/orders.html"


class DownloadsView(TemplateView):
    template_name: str = "frontend/account/downloads.html"


class AddressesView(TemplateView):
    template_name: str = "frontend/account/addresses.html"


class AccountDetails(TemplateView):
    template_name: str = "frontend/account/account-detailes.html"


class WishlistView(ListView):
    model = frontend_model.wishlist
    template_name: str = "frontend/account/wishlist.html"
    context_object_name = "wishlist"

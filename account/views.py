from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from frontend.models import wishlist as frontend_wishlist
from cpanel.models import order
from django.views.generic.detail import DetailView


# Create your views here.
class AccountHomeView(TemplateView):
    template_name: str = "frontend/account/dashboard.html"


class OrderView(ListView):
    model = order
    template_name: str = "frontend/account/orders.html"
    context_object_name = "account_orders"
    paginate_by = 20
    ordering = ["-created_at"]
    # queryset = model.

    def get_queryset(self):
        return order.objects.filter(email=self.request.user.email).order_by(
            "-created_at"
        )[0:20]


class order_account_details(TemplateView):
    template_name = "frontend/account/order_account_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context["order"] = order.objects.filter(orderid=context["orderid"]).first()
        return context

    # def get_queryset(self):
    #     print(self.context)
    #     # return order.objects.filter(orderid=kwargs["orderid"])


class DownloadsView(TemplateView):
    template_name: str = "frontend/account/downloads.html"


class AddressesView(TemplateView):
    template_name: str = "frontend/account/addresses.html"


class AccountDetails(TemplateView):
    template_name: str = "frontend/account/account-detailes.html"


class WishlistView(ListView):
    model = frontend_wishlist
    template_name: str = "frontend/account/wishlist.html"
    context_object_name = "wishlist"

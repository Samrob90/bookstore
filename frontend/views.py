from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from cpanel import models as cpanel_model
from math import ceil
from django.views.generic.detail import DetailView


class HomeVIew(TemplateView):
    template_name = "frontend/home.html"


# change to list view when model is ready
class ShopView(ListView):
    template_name = "frontend/shop.html"
    model = cpanel_model.book
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["range"] = range(
            1, ceil(cpanel_model.book.objects.all().count() / 4) + 1
        )
        return context


class ProductView(DetailView):
    template_name = "frontend/product_single.html"
    model = cpanel_model.book
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context["book_images"] = cpanel_model.bookimages.objects.filter(book=book)
        context["details"] = cpanel_model.bookdetails.objects.filter(book=book)

        return context


class AboutView(TemplateView):
    template_name = "frontend/about.html"


class ContactView(TemplateView):
    template_name = "frontend/contact.html"


class FaqView(TemplateView):
    template_name = "frontend/faq.html"

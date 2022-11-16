from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView


class HomeVIew(TemplateView):
    template_name = "frontend/home.html"


# change to list view when model is ready
class ShopView(TemplateView):
    template_name = "frontend/shop.html"
    # model = None
    # paginate_by = 100


class AboutView(TemplateView):
    template_name = "frontend/about.html"


class ContactView(TemplateView):
    template_name = "frontend/contact.html"


class FaqView(TemplateView):
    template_name = "frontend/faq.html"

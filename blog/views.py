from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

# Create your views here.


class BlogIndex(TemplateView):
    template_name = "frontend/blog/index.html"

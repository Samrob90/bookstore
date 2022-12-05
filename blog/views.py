from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import blog

# Create your views here.


class BlogIndex(ListView):
    template_name = "frontend/blog/index.html"
    model = blog
    context_object_name = "blog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get("category")
        if category is not None:
            context["blog"] = blog.objects.filter(category__contains=str(category))

        return context


class BlogDetail(DetailView):
    template_name: str = "frontend/blog/blog_detail.html"
    model = blog
    context_object_name = "blog"

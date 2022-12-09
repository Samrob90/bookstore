from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import blog, blog_comment
from .forms import Comments
from django.contrib import messages


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


class BlogDetail(TemplateView):
    template_name: str = "frontend/blog/blog_detail.html"
    form = Comments()

    def get(self, request, *args, **kwargs):
        context = {
            "blog": blog.objects.get(blogid=kwargs["uuid"], slug=kwargs["slug"]),
            "form": self.form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = Comments(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if self.validateEmail(email):

                fullname = form.cleaned_data.get("fullname")
                comment = form.cleaned_data.get("comment")
                blog_ = blog.objects.filter(blogid=kwargs["uuid"]).first()
                print(blog_)

                blog_comment.objects.create(
                    blog=blog_, fullname=fullname, email=email, comment=comment
                )
                messages.success(request, "Comment submited successfuly")
            else:
                messages.error(request, "Invalide email address ")
        context = {
            "blog": blog.objects.get(blogid=kwargs["uuid"], slug=kwargs["slug"]),
            "form": form,
        }
        return render(request, self.template_name, context)

    def validateEmail(self, email):
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError

        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

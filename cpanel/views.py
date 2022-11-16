from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from . import form
from django.contrib.auth import authenticate, login, logout
from authentications.models import Account
from django.contrib import messages

# Create your views here.

# cpanel login
class CpanelLoginView(TemplateView):
    template_name = "cpanel/accounts/login.html"
    class_form = form.LoginForm

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, {"form": self.class_form})

    def post(self, request, *args, **kwargs):
        form = self.class_form(request.POST)
        if form.is_valid():
            """
            .To authenticate user with username
            .first we check if username exist then get email of username
            .then authenticate user with the email
            """
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print(username)
            print(password)
            # print(Account.objects.get(username))

            email = Account.objects.filter(username=username).first()
            if email is not None:
                user = authenticate(request, email=email.email, password=password)
                if user:
                    if user.is_staff or user.is_superuser or user.is_admin:
                        login(request, user)
                        return redirect("cpanel_dashboard")
                    else:
                        messages.error(
                            request,
                            "You do not have permition to access this page. ",
                        )
                else:
                    messages.error(request, "Incorrect username or password.")
            else:
                messages.error(request, "Incorrect username or password")

        else:
            messages.error(request, "Incorrect username or password.")

        return render(request, self.template_name, {"form": form})


class CpanelDashboardView(TemplateView):
    template_name = "cpanel/home/content/dashboard.html"


class CpanelBooksView(TemplateView):
    template_name = "cpanel/home/content/book.html"


class CpanelAddbookView(TemplateView):
    template_name = "cpanel/home/content/add-book.html"
    class_form = form.BooksForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.class_form})


class CpanelLogoutVIew(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect("cpanel_login")

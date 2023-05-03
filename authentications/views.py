from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from . import forms
from django.contrib.auth import authenticate, login, logout

# import token
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .tokenGenerator import account_activation_token
from dotenv import load_dotenv
import os
from authentications import models
from rsc.SendMail import SendMail
from django.contrib.auth import get_user_model
from django.contrib import messages
from . import tasks
from django.utils import timezone
from datetime import timedelta
from frontend import tasks as frontend_tasks
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.backends import ModelBackend


load_dotenv()


# Create your views here.
class LoginView(TemplateView):
    template_name = "frontend/authentication/login.html"
    class_form = forms.LoginForm()
    next = None

    def get(self, request, *args, **kwargs):
        global next
        next = request.GET.get("next", None)
        return render(request, self.template_name, {"form": self.class_form})

    def post(self, request, *args, **kwargs):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.email_verify:
                    if "cart" in request.session:
                        tasks.check_cart.delay(request.session["cart"], user.pk)
                    if "recent_view" in request.session:
                        frontend_tasks.check_recent_view(
                            request.session["recent_view"], user.pk
                        )
                    login(
                        request,
                        user,
                        backend="django.contrib.auth.backends.ModelBackend",
                    )

                    return self.redirect_after_login(request)
                else:
                    return redirect("verify_email")
            else:
                messages.error(request, "Incorrect email or password")
        else:
            messages.error(request, "Incorrect email or password")
        return render(request, self.template_name, {"form": form})

    # check for vulbability here before production
    def redirect_after_login(self, request):
        next = request.GET.get("next", None)
        if next is None:
            return redirect("account")
        elif not url_has_allowed_host_and_scheme(
            url=next,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect("account")
        else:
            return redirect(next)


class SignUpView(TemplateView):
    template_name = "frontend/authentication/signup.html"
    class_form = forms.RegisterForm()

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": forms.RegisterForm()})

    def post(self, request, *args, **kwargs):
        form = forms.RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_google_auth = False
            user.email_verify = False
            user.save()
            email = form.cleaned_data.get("email")
            data = {
                "last_name": user.last_name,
                "domain": "newtonbookshop.com",
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            }

            mail_data = {
                "data": data,
                "email": email,
                "subject": "Please verify your email address",
                "template_name": "frontend/email/verification_email_link.html",
                "send_from": os.getenv("SECURITY_EMAIL_SENDER"),
            }
            tasks.registration_verify_email.delay(mail_data)
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(
                request,
                f"Your account has been successfully created. A confirmation link has been sent to {email}. Please confirm it to complete your registration",
            )
            return redirect("verify_email")

        return render(request, self.template_name, {"form": form})


class ActivateView(TemplateView):
    template_name = "frontend/authentication/activate.html"

    def get(self, request, *args, **kwargs):
        uidb64 = kwargs["uidb64"]
        token = kwargs["token"]
        User = get_user_model()
        account_verify = False
        account_already_verify = False
        account_invalide = False

        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        time_expired = None
        if user is not None:
            time_expired = user.last_updated + timedelta(minutes=45)

        if user is not None and user.email_verify == True:
            account_already_verify = True

        if user is None:
            account_invalide = True

        if (
            user is not None
            and time_expired < timezone.now()
            and user.email_verify == False
        ):
            account_invalide = True

        if (
            user is not None
            and user.email_verify == False
            and account_activation_token.check_token(user, token)
            and time_expired > timezone.now()
        ):
            user.email_verify = True
            user.save()
            account_verify = True

        print(account_invalide, account_already_verify, account_invalide)
        context = {
            "account_verify": account_verify,
            "account_already_verify": account_already_verify,
            "account_invalide": account_invalide,
        }

        return render(request, self.template_name, context)


class VerifyEmailView(TemplateView):
    template_name: str = "frontend/email_verification/verify_email.html"

    def get(self, request, *args, **kwargs):
        if request.user and request.user.email_verify == True:
            return redirect("account")
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.user.email
        data = {
            "last_name": str(request.user.last_name),
            "domain": "newtonbookshop.com",
            "uid": urlsafe_base64_encode(force_bytes(request.user.pk)),
            "token": account_activation_token.make_token(request.user),
        }

        mail_data = {
            "data": data,
            "email": email,
            "subject": "Please verify your email address",
            "template_name": "frontend/email/verification_email_link.html",
            "send_from": os.getenv("SECURITY_EMAIL_SENDER"),
        }
        tasks.registration_verify_email.delay(mail_data, request.user.pk)
        messages.success(
            request,
            f"A confirmation link has been sent to {email}. Please confirm it to complete your registration",
        )
        return redirect("verify_email")


class ChangeEmail(TemplateView):
    template_name: str = "frontend/email_verification/change_verification_email.html"
    class_form = forms.ChangeEmail()

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.class_form})

    def post(self, request, *args, **kwargs):
        form = forms.ChangeEmail(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")

            if models.Account.objects.filter(email=email).exists():
                messages.error(request, "This this email address is aready taken ")
            else:
                user = models.Account.objects.filter(email=request.user.email).update(
                    email=email
                )
                messages.success(
                    request,
                    "Email updated successfully ! You can now send a verification link to your new email address",
                )
                return redirect("verify_email")
        return render(request, self.template_name, {"form": form})


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")

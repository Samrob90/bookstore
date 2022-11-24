from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from . import forms
from django.http import HttpResponse, JsonResponse
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

load_dotenv()
# Create your views here.
class LoginView(TemplateView):
    template_name = "frontend/account/login.html"


class SignUpView(TemplateView):
    template_name = "frontend/account/signup.html"
    class_form = forms.RegisterForm()

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": forms.RegisterForm()})

    def post(self, request, *args, **kwargs):
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
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
            login(request, user)
            messages.success(
                request,
                f"Your account has been successfully created. A confirmation link has been sent to <stronge>{email}<stronge>. <br>Please confirm it to complete your registration",
            )
            return redirect("verify_email")

        return render(request, self.template_name, {"form": form})


class ActivateView(TemplateView):
    template_name = "frontend/account/activate.html"

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
        if user is not None and user.email_verify == True:
            account_already_verify = True

        # check email time frame here
        if user is None:
            account_invalide = True

        if (
            user is not None
            and user.email_verify == False
            and account_activation_token.check_token(user, token)
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
        tasks.registration_verify_email.delay(mail_data)
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

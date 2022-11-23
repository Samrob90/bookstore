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
                "user": user,
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
            mail = SendMail(data=mail_data)
            mail.send()
            return redirect("/verify_email")

        return render(request, self.template_name, {"form": form})


class ActivateView(TemplateView):
    template_name = "frontend/account/activate.html"

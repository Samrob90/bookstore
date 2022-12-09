from django import forms
from .models import blog_comment


class Comments(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Enter your comment",
                "class": "form-control rounded-0 px-4",
                "rows": "8",
            }
        )
    )

    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your full name",
                "class": "form-control rounded-0 px-4",
            }
        )
    )

    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your Email",
                "class": "form-control rounded-0 px-4",
            }
        )
    )

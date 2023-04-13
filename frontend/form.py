from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from .models import contact_us


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Full name"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter your email address"}
        )
    )
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Subject"}
        ),
    )
    message = forms.CharField(
        max_length=100,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your message",
                "rows": "6",
                "cols": 77,
            }
        ),
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta(object):
        model = contact_us
        fields = ("name", "email", "subject", "message", "captcha")

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["subject"].widget.attrs["class"] = "form-control"
        self.fields["message"].widget.attrs["class"] = "form-control"

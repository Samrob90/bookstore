from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


class SendMail:
    def __init__(self, **kwargs):

        self.data = kwargs["data"]
        self.email = kwargs["email"]
        self.subject = kwargs["subject"]
        self.template_name = kwargs["template_name"]
        self.content = render_to_string(self.template_name, {"data": self.data})
        self.send_from = f"Newtonbookshop <{kwargs['send_from']}>"

    def Imsend(self):
        text_tags = strip_tags(self.content)
        return text_tags

    def send(self):
        to = self.email
        email = EmailMultiAlternatives(
            self.subject, self.Imsend(), self.send_from, [to]
        )
        email.attach_alternative(self.content, "text/html")
        email.send()
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


class SendMail:
    def __init__(self, **kwargs):

        self.data = kwargs["data"]["data"]
        self.email = kwargs["data"]["email"]
        self.subject = kwargs["data"]["subject"]
        self.template_name = kwargs["data"]["template_name"]
        self.content = render_to_string(self.template_name, {"data": self.data})
        self.send_from = f"Newtonbookshop <{kwargs['data']['send_from']}>"

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

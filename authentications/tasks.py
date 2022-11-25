from urllib import request
from celery import shared_task
from rsc.SendMail import SendMail
from time import sleep
from urllib.request import Request, urlopen
from authentications import models
import time
from django.utils import timezone

from . import models


@shared_task()
def registration_verify_email(data, user_id=None):
    # user = models.Account.objects.filter(pk=user_id)
    # last_name = data["data"]["last_name"] = user.last_name
    # print(last_name)
    if user_id is not None:
        user = models.Account.objects.filter(pk=user_id).update(
            last_updated=timezone.now()
        )
    SendMail(data=data)
    return "done"

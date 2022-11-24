from urllib import request
from celery import shared_task
from rsc.SendMail import SendMail
from time import sleep
from urllib.request import Request, urlopen
from authentications import models
import time

from . import models


@shared_task()
def registration_verify_email(data):
    # user = models.Account.objects.filter(pk=user_id)
    # last_name = data["data"]["last_name"] = user.last_name
    # print(last_name)
    print("sleeping for 20 seconds")
    time.sleep(20)
    SendMail(data=data)
    return "done"


# @shared_task()
# def test_func():
#     sam = 10 + 34
#     return "Done"

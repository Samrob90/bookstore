import requests, os, json
from dotenv import load_dotenv
from cpanel.models import transaction, order

load_dotenv()


class VerifyTransaction:
    def __init__(self, reference):
        self.reference = reference
        self.URL = f"https://api.paystack.co/transaction/verify/{self.reference}"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('paystack_secretkey_text')}",
            "Cache-Control": "no-cache",
        }
        self.verify()

    def verify(self):
        responses = requests.get(self.URL, headers=self.headers)
        response = json.loads(responses.content)

        if response["status"] == True:
            self.save_transaction(response["data"])
            if response["data"]["status"] == "success":
                return True

    def save_transaction(self, data):
        # get fetch order
        order_obj = order.objects.get(orderid=self.reference)

        # then update transaction object value
        transaction.objects.filter(order=order_obj).update(
            status=data["status"], data=json.dumps(data)
        )

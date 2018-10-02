import unittest
import json

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import RequestsClient

from shop.models.wallet import Wallet
from registrations.models import Participant, College
from shop.models.order import Order, OrderFragment
from shop.models.stall import Stall
from shop.models.item import ItemClass
from shop.models.transaction import Transaction

# Not the most complete or beautiful tests
# but they're still pretty useful.
# Only testing the expected-to-be-successful cases and not the others due to severe time constraints

CACHE = dict()

class ShopTests(TestCase):

    def setUp(self):
        # create a user named Wong, and one named Dr. Stephen Strange.
        u1 = User(username="wong")
        u1.set_password("asdfghjkl")
        u1.save()

        u2 = User(username="strange")
        u2.set_password("asdfghjkl")
        u2.save()

        # make a college
        c = College.objects.create(name="University of Kamar Taj")

        # make a Wong and Strange participants
        p1 = Participant.objects.create(
                            name="Wong",
                            gender="Male",
                            city="Hong Kong",
                            email="wong@gmail.com",
                            college=c,
                            phone="1234567890",
                            user=u1,
                            firewallz_passed=True
                        )

        p2 = Participant.objects.create(
                            name="Dr. Stephen Strange",
                            gender="Male",
                            city="New York",
                            email="strange@gmail.com",
                            college=c,
                            phone="0987654321",
                            user=u2,
                            firewallz_passed=True
                        )

        u1.wallet.balance.add(1000,500,500,500)
        u2.wallet.balance.add(1000,500,500,500)

        # create a stall user for Baskin Robbins
        su = User(username="baskin")
        su.set_password("asdfghjkl")
        su.save()

        # create the Baskin Robbins stall and add something to its menu
        s = Stall.objects.create(user=su, name="Baskin Robbins")
        i = s.menu.create(name="Single Scoop Ice Cream", stall=su, is_veg=True, price=70)


    def test_participant_login(self):
        """ checks:
                1. status 200 response
                2. a jwt, qr code and id are returned in the response """

        client = RequestsClient()
        headers = {"Wallet-Token": "asdf", "Content-Type": "application/json"}

        data = {"username": "wong", "password": "asdfghjkl", "is_bitsian": False}
        response = client.post("http://testserver/shop/auth/", json=data, headers=headers)

        self.assertTrue(response.status_code == 200)

        response = json.loads(response.text)
        all_in = all(["user_id" in response, "token" in response, "qr_code" in response])

        self.assertTrue(all_in)

        headers["Authorization"] =  "JWT {}".format(response["token"])

        CACHE["headers"] = headers


    def test_place_order_succesfully(self):
        """ check for the following:
                1. The response is of status 200
                2. The response is as expected """

        user = User.objects.get(username="wong")

        initial_balance = user.wallet.getTotalBalance()

        order = {
            "date": "October 18th, 2018",
            "order": {
                "1": {
                    "name": "Baskin Robbins",
                    "items": [{
                        "id": 1,
                        "name": "Single Scoop Ice Cream",
                        "price": 70,
                        "qty": 5
                    }]
                }
            },
            "price": 350
        }

        client = RequestsClient()
        headers = CACHE["headers"]
        response = client.post("http://testserver/shop/place-order/", json=order, headers=headers)

        self.assertTrue(response.status_code == 200)

        response = json.loads(response.text)

        ideal_response = {
                            "cost": 350,
                            "order_id": 1,
                            "fragments_ids": [
                                {
                                    "id": 1,
                                    "stall_id": 1
                                }
                            ]
                        }

        self.assertEqual(response, ideal_response)

        user = User.objects.get(username="wong")
        # refreshing the user like this is VERY important here

        final_balance = user.wallet.getTotalBalance()

        self.assertTrue(initial_balance - final_balance == response["cost"])


    def test_transfer_succesfully(self):
        """ check for the following:
                1. The response is of status 200
                2. The transfer has executed successfully
                3. A transaction instance has been made for it """

        wong_initial = Wallet.objects.get(user__username="wong").getTotalBalance()
        strange_intial = Wallet.objects.get(user__username="strange").getTotalBalance()

        details = {"target_user": 2, "amount": 300}

        client = RequestsClient()
        headers = CACHE["headers"]
        response = client.post(
                                url="http://testserver/shop/transfer/",
                                json=details,
                                headers=headers
                            )

        self.assertEqual(response.status_code, 200)

        response = json.loads(response.text)

        wong_wallet = Wallet.objects.get(user__username="wong")
        strange_wallet = Wallet.objects.get(user__username="strange")

        wong_final = wong_wallet.getTotalBalance()
        strange_final = strange_wallet.getTotalBalance()

        self.assertTrue(wong_initial-300 == wong_final)
        self.assertTrue(strange_intial+300 == strange_final)

        try:
            transaction = Transaction.objects.get(
                                    transfer_from=wong_wallet,
                                    transfer_to=strange_wallet,
                                    transfer_type="transfer",
                                    amount=300
                                )
        except Transaction.DoesNotExist:
            transaction = False

        self.assertTrue(transaction)

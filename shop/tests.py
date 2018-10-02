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

CACHE = dict()

class ShopTests(TestCase):
    # Test placing orders as a participant
    # Not the most complete or beautiful test but it's pretty useful.
    # Especially for a first test.

    def setUp(self):
        # create a user named Wong.
        u = User(username="wong")
        u.set_password("asdfghjkl")
        u.save()

        # make a college
        c = College.objects.create(name="University of Kamar Taj")

        # make a Wong a participant
        p = Participant.objects.create(
                            name="Wong",
                            gender="Male",
                            city="Hong Kong",
                            email="wong@gmail.com",
                            college=c,
                            phone="1234567890",
                            user=u,
                            firewallz_passed=True
                        )

        u.wallet.balance.add(1000,500,500,500)

        # create a stall user for Baskin Robbins
        su = User(username="baskin")
        su.set_password("asdfghjkl")
        su.save()

        # create the Baskin Robbins stall and add something to its menu
        s = Stall.objects.create(user=su, name="Baskin Robbins")
        i = s.menu.create(name="Single Scoop", stall=su, is_veg=True, price=70)

        CACHE["username"] = u.username
        CACHE["participant"] = p
        CACHE["stall_user"] = su
        CACHE["stall"] = s
        CACHE["item"] = i


    def test_participant_login(self):
        """ checks:
                1. status 200 response
                2. a jwt, qr code and id are returned """

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
                2. The response contains """

        user = User.objects.get(username=CACHE["username"])

        initial_balance = user.wallet.getTotalBalance()

        order = {
            "date": "October 18th, 2018",
            "order": {
                "1": {
                    "name": "Baskin Robbins",
                    "items": [{
                        "id": 1,
                        "name": "Single Scoop",
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

        user = User.objects.get(username=CACHE["username"])
        # refreshing the user like this is VERY important here

        final_balance = user.wallet.getTotalBalance()

        self.assertTrue(initial_balance - final_balance == response["cost"])

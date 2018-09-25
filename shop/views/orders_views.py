import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from shop.models.order import Order, OrderFragment
from shop.models.stall import Stall
from shop.models.item import ItemClass, ItemInstance, Tickets
from shop.models.transaction import Transaction
from shop.permissions import TokenVerification
from utils.wallet_qrcode import decString
from events.models import MainProfShow


class PlaceOrder(APIView):
    """ The main view to handle orders. For the structure expected from the
        app/front-end teams, see the below """

    permission_classes = (IsAuthenticated, TokenVerification,)

    @csrf_exempt ### REMOVE THIS SOON
    def post(self, request, format=None):
        """
            Part 1:
            Create a new Order (it acts as a shell), then create all of the
            OrderFragments while populating each fragment with Item Instances.
            If any item is unavailable, bounce back the entire order, the
            frontend team shouldn't let it get this far.

            Part 2:
            Figure out how much the Order costs, test to see if the customer
            has enough funds. Then if not, delete the entire Order, and return
            an error message. Else, generate transactions and return the
            Order's id so that it can be queried against firestore.

        """

        # Part 1:
        try:
            data = request.data["order"]
        except KeyError as missing:
            msg = {"message": "missing the following field: {}".format(missing)}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        customer = request.user.wallet

        order = Order.objects.create(customer=customer)

        for stall_id, stall in data.items():
            try:
                stall_instance = Stall.objects.get(id = stall_id)
            except Stall.DoesNotExist:
                order.delete()
                msg = {"message" : "Stall doesn't exist"}
                return Response(msg, status = status.HTTP_404_NOT_FOUND)

            fragment = order.fragments.create(stall=stall_instance, order=order)

            for item in stall["items"]:
                try:
                    itemclass = ItemClass.objects.get(id=item["id"])
                except:
                    msg = "invalid item id {}".format(item["id"])
                    stat = status.HTTP_404_NOT_FOUND
                    order.delete()
                    return Response({"message": msg}, status=stat)

                if not itemclass.is_available:
                    msg = {"message":"{} is not currently available".format(itemclass)}
                    stat = status.HTTP_404_NOT_FOUND
                    order.delete()
                    return Response(msg, status=stat)

                try:
                    qty = item["qty"]
                except KeyError:
                    msg = {"message" : "Quantity of item: #{} wasn't specified.".format(item["id"])}
                    return Response(msg, status = status.HTTP_404_NOT_FOUND)

                fragment.items.create(itemclass=itemclass, quantity=item["qty"], order=fragment)

            fragment.save() # to perform some extra synchronization with firestore

        # Part 2:
        net_cost = order.calculateTotal()
        total_balance = request.user.wallet.getTotalBalance()

        if total_balance < net_cost:
            msg = {"message": "Insufficient balance.", "missing_funds":net_cost-total_balance},
            stat = status.HTTP_400_BAD_REQUEST
            order.delete()
            return Response(msg, stat)

        for fragment in order.fragments.all():
            # Create transaction instances and deduct money from the user right
            # away. Then later, once the order has been complete, the stall
            # will receive its money.
            Transaction.objects.create(
                                        amount=fragment.calculateSubTotal(),
                                        transfer_to=fragment.stall.user.wallet,
                                        transfer_type="buy",
                                        transfer_from=request.user.wallet
                                    )
        request.user.wallet.balance.deduct(net_cost)
        fragments = [fragment.id for fragment in order.fragments.all()]


        data["order_id"] = order.id
        data["fragment_ids"] = fragments
        data["date"] = request.data["date"]
        order.setQueryString({"order": data})

        return Response({"order_id": order.id, "fragments_ids": fragments, "cost": net_cost})


class GetOrders(APIView):

    permission_classes = (IsAuthenticated, TokenVerification,)

    @csrf_exempt
    def get(self, request):
        data = dict()
        data["orders"] = list()
        for order in request.user.wallet.orders.all():
            try:
                data["orders"].append(order.getQueryString())
            except TypeError: # no query string e.g. orders made via. admin panal
                pass
        return Response(data, status=status.HTTP_200_OK)


class GetTickets(APIView):

    permission_classes = (TokenVerification,) # Extra form of verification needed? Only allow departments to access this endpoint?

    @csrf_exempt
    def post(self, request):
        qr_code = request.data["qr_code"]
        user_id = decString(qr_code)[0]        # a custom function from utils.wallet_qrcode
        user = get_object_or_404(User, id=user_id)

        try:
            tickets = {"tickets": []}
            for ticket in user.tickets.all():
                tickets["tickets"].append({
                                            "show_id": ticket.prof_show.id,
                                            "show_name": ticket.prof_show.name,
                                            "number_of_tickets": ticket.count
                                        })
        except:
            return Response({"message": "user has no tickets."})

        return Response(tickets, status=status.HTTP_200_OK)


class ConsumeTickets(APIView):
    """ The endpoint which is called for scanning and deducting tickets.
        sample request:
            {
                "qr_code": "gAAAAABbpxxqQKmaLjQdoCWlbwif6WNzbvZgjiemu8qG7-UhaCAW6DMaEQROYMRX5A10X_wDnxcDNRnn4QS49CVOVCme8Gu3vCIvKNwDhWEwmw995nMGl0U=OASIS18",
                "consume": 3,
                "show_id": 1
           }
    """

    permission_classes = (TokenVerification,) # Extra form of verification needed? Only allow departments to access this endpoint?

    @csrf_exempt
    def post(self, request):
        qr_code = request.data["qr_code"]
        user_id = decString(qr_code)[0]
        user = get_object_or_404(User, id=user_id)
        show = get_object_or_404(MainProfShow, id=request.data["show_id"])
        tickets = get_object_or_404(Tickets, user=user, prof_show=show)
        consume = request.data["consume"]

        max_count = tickets.count
        if(consume > max_count):
            return Response({"success": False, "max_tickets": max_count})
        tickets.count -= consume
        tickets.save()
        return Response({"success": True, "remaining_tickets": tickets.count})

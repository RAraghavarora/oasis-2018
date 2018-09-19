from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from shop.models.order import Order, OrderFragment
from shop.models.stall import Stall
from shop.models.item import ItemClass, ItemInstance
from shop.models.transaction import Transaction
from shop.permissions import TokenVerification


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
            stall_instance = Stall.objects.get(id=stall_id)
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

                fragment.items.create(itemclass=itemclass, quantity=item["qty"], order=fragment)

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
                                        amount=net_cost,
                                        transfer_to=fragment.stall.user.wallet,
                                        transfer_type="buy",
                                        transfer_from=request.user.wallet
                                    )
            request.user.wallet.balance.deduct(net_cost)
        fragments = [fragment.id for fragment in order.fragments.all()]

        return Response({"order_id": order.id, "fragments_ids": fragments, "cost": net_cost})

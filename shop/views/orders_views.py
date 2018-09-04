from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from shop.models.order import Order, OrderFragment


class PlaceOrder(APIView):
    """ The main view to handle orders. For the structure expected from the
        app/front-end teams, see the below """

    def post(self, request, format=None):
        """
            Part 1:
            Create a new Order (it acts as a shell), then create all of the
            OrderFragments with a status of in-review by default while
            populating each fragment with Item Instances.
            Then figure out how much the Order costs.

            Part 2:
            Test to see if the customer has enough funds. Then if not, delete
            the entire Order, and return an error message. Else, generate
            transactions and return a the Order object (serialized).

        """

        data = request.data["order"]

        # Part 1: popluate an order
        customer = request.user.wallet
        order = Order.objects.create(customer=customer)
        for stall in data:
            fragments = OrderFragment.objects.create(
                                            stall=Stall.objects.get(id=stall),
                                            order=order, transaction=None
                                        )
            for item in stall[items]:
                item = ItemInstance.objects.create(
                                itemclass=ItemClass.objects.get(id=item[id]),
                                quantity=item[quantity],
                                order=fragment)
                )

        # Part 2: check balance and populate transactions
        total_due = order.calculateTotal()
        if(customer._getTotalBalance < total_due):
            # TODO: log it
            return Response(
                            data={"message": "Insufficient Funds"},
                            status=status.HTTP_412_PRECONDITION_FAILED
                        )
        order.generateTransactions()

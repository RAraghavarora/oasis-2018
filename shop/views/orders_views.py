from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from utils.wallet import transferHelper
from shop.models.order import Order, OrderFragment
from shop.permissions import TokenVerification


@csrf_exempt # maybe find a way to remove this?
@login_required
class PlaceOrder(APIView):
    """ The main view to handle orders. For the structure expected from the
        app/front-end teams, see the below """

    permission_classes = (IsAuthenticated, TokenVerification,)

    def post(self, request, format=None):
        """
            Part 1:
            Create a new Order (it acts as a shell), then create all of the
            OrderFragments with a status of in-review by default while
            populating each fragment with Item Instances. If any item is
            unavailable, bounce back the entire order, the frontend team
            shouldn't let it get this far.

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
        for stall in data:
            stall_id = Stall.objects.get(id=stall.key())
            fragment = OrderFragment.objects.create(
                                                    stall=stall_id,
                                                    order=order,
                                                )
            for item in stall["items"]:
                itemclass = ItemClass.objects.get(id=item["id"])
                if not itemclass.is_available:
                    msg = {"message":"{} is not available".format(itemclass)}
                    stat = status.HTTP_417_EXPECTATION_FAILED
                    order.delete()
                    return Response(msg, status=stat)
                ItemInstance.objects.create(
                                        itemclass=itemclass,
                                        quantity=item["quantity"],
                                        order=fragment
                                    )

        # Part 2:
        net_cost = order.calculateTotal()
        if request.user.wallet.getTotalBalance() < net_cost:
            msg = {"message": "Insufficient balance."},
            stat = status.HTTP_412_PRECONDITION_FAILED
            return Response(msg, stat)
        for fragment in order.fragments.all():
            transferHelper({
                        "source-id": request.user.wallet.id,
                        "target-id": fragment.stall.user.wallet.id,
                        "amount": fragment.calculateSubTotal,
                    })
        fragments = [fragment.id for fragment in order.fragments.all()]
        return Response({"order_id": order.id, "fragments": fragments})
        # NOW NOTIFY THE STALL?

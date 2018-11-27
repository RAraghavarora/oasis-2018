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
from shop.models.wallet import Wallet
from shop.models.item import ItemClass, ItemInstance, Tickets
from shop.models.transaction import Transaction, TicketTransaction
from shop.permissions import TokenVerification
# from utils.wallet_qrcode import decString
from events.models import MainProfShow, Organization
from registrations.models import Bitsian

from random import randint

class PlaceOrder(APIView):
    """ The main view to handle orders. For the structure expected from the
        app/front-end teams, see the below """

    permission_classes = (IsAuthenticated, TokenVerification,)

    def generate_otp(self):
        return randint(1000, 9999)

    @csrf_exempt
    def post(self, request, format=None):
        """
            Part 1:
            Create a new Order (it acts as a shell), then create all of the
            OrderFragments while populating each fragment with Item Instances.
            If any item is unavailable, bounce back the entire order, the
            frontend team shouldn't let it get this far.

            NOTE: special considerations have to be given to prof show tickets

            Ticket Vendor stall
            sells tickets by name but these are normal items/itemclasses
            but we also get or create the Ticket instance during the place-order call
            and increment count as needed after performing extra checks on availability

            Part 2:
            Figure out how much the Order costs, test to see if the customer
            has enough funds. Then if not, delete the entire Order, and return
            an error message. Else, generate transactions and return the
            Order's id so that it can be queried against firestore.

        """

        ### Needed: extra checks to see it the item belongs to that stall or not

        # Part 1:
        try:
            data = request.data["order"]
        except KeyError as missing:
            msg = {"message": "missing the following field: {}".format(missing)}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        customer = request.user.wallet

        order = Order.objects.create(customer=customer)

        flag = True
        unavailable = []
        tickets_actions = []

        for stall_id, stall in data.items():
            try:
                stall_instance = Stall.objects.get(id = stall_id)
            except Stall.DoesNotExist:
                order.delete()
                msg = {"message" : "Stall with the following id doesn't exist: {}".format(stall_id)}
                return Response(msg, status = status.HTTP_404_NOT_FOUND)

            otp = self.generate_otp()

            if flag:
                fragment = order.fragments.create(stall=stall_instance, order=order, otp = otp)

            for item in stall["items"]:
                try:
                    itemclass = ItemClass.objects.get(id=item["id"])
                    qty = int(item["qty"])
                    if qty < 0:
                        raise ValueError
                except KeyError as missing:
                    msg = {"message" : "The following field was missing: {}".format(missing)}
                    order.delete()
                    return Response(msg, status = status.HTTP_404_NOT_FOUND)
                except ItemClass.DoesNotExist:
                    msg = "Item with the following id doesn't exist: {}".format(item["id"])
                    order.delete()
                    return Response({"message": msg}, status = status.HTTP_404_NOT_FOUND)
                except ValueError:
                    msg = {"message" : "Wrong values."}
                    order.delete()
                    return Response(msg, status = status.HTTP_400_BAD_REQUEST)

                if stall_instance.name == "Prof Shows":
                    try:
                        shows = [MainProfShow.objects.get(name=ic) for ic in itemclass.name.split(" + ")]
                        for show in shows:
                            ic = ItemClass.objects.get(name=show.name)
                            if any([not ic.is_available, ic.stock < qty]):
                                raise MainProfShow.DoesNotExist
                            if flag:
                                tickets, _ = Tickets.objects.get_or_create(user=request.user, prof_show=show)
                                tickets_actions.append([tickets, show, itemclass, qty])
                    except MainProfShow.DoesNotExist:
                        unavailable.append(itemclass.id)
                        flag = False

                else:
                    if not itemclass.is_available:
                        unavailable.append(itemclass.id)
                        flag = False

                #Name of the stalls for Mess will be stored as: "XYZ Mess"
                if stall_instance.name[-4:].title() == "Mess":
                    if qty > itemclass.stock:
                        msg = {"message" : "Not enough stock."}
                        return Response(msg, status=status.HTTP_404_NOT_FOUND)
                    elif flag:
                        itemclass.stock -= qty
                        itemclass.save()

                if flag:
                    fragment.items.create(itemclass=itemclass, quantity=item["qty"], order=fragment)

            if flag:
                fragment.save() # to perform some extra synchronization with firestore

        if unavailable:
            order.delete()
            dump = json.dumps({"unavailable" : unavailable}, sort_keys=True, separators=(',', ': '))
            load = json.loads(dump)
            return Response(load, status = status.HTTP_424_FAILED_DEPENDENCY)


        # Part 2:
        net_cost = order.calculateTotal()
        print(net_cost)
        total_balance = request.user.wallet.getTotalBalance()

        if total_balance < net_cost:
            msg = {"message": "Insufficient balance.", "missing_funds":net_cost-total_balance}
            stat = status.HTTP_400_BAD_REQUEST
            order.delete()
            return Response(msg, stat)

        for fragment in order.fragments.all():
            # Create transaction instances and deduct money from the user right
            # away. Then later, once the order has been complete, the stall
            # will receive its money.
            # The Ticket Vendor must, however, receive their money right away
            if fragment.stall.name == "Prof Shows":
                fragment.status = OrderFragment.FINISHED
                fragment.stall.user.wallet.balance.add(transfers=fragment.calculateSubTotal())
                fragment.save()
            t = Transaction.objects.create(
                                        amount=fragment.calculateSubTotal(),
                                        transfer_to=fragment.stall.user.wallet,
                                        transfer_type="buy",
                                        transfer_from=request.user.wallet
                                    )
            fragment.transaction = t
            fragment.save()
        customer.balance.deduct(net_cost)
        fragments = [{"id": fragment.id, "stall_id": fragment.stall.id} for fragment in order.fragments.all()]

        print("tickets actions:")
        print(tickets_actions)
        for action in tickets_actions:
            show = action[1]
            ticket = Tickets.objects.get(user=request.user, prof_show=show)
            itemclass = action[2]
            qty = action[3]
            ticket.count += qty
            print(ticket.count)
            show.tickets_sold += qty
            itemclass.stock -= qty
            ticket.save()
            show.save()
            itemclass.save()

        return Response({"order_id": order.id, "fragments_ids": fragments, "cost": net_cost})


class GetOrders(APIView):

    permission_classes = (IsAuthenticated, TokenVerification,)

    @csrf_exempt
    def get(self, request):
        response = dict()
        response["orders"] = list()
        for order in request.user.wallet.orders.all():
            data = dict()
            data["order_id"] = order.id
            data["price"] = order.calculateTotal()
            data["date"] = order.timestamp
            data["fragment_ids"] = [{"stall_id": fragment.stall.id, "status": fragment.status, "id": fragment.id} for fragment in order.fragments.all()]
            data["order"] = dict()
            for fragment in order.fragments.all():
                data["order"][str(fragment.stall.id)] = dict()
                data["order"][str(fragment.stall.id)]["items"] = [{"qty": item.quantity, "name": item.itemclass.name, "price": item.calculatePrice(), "id": item.itemclass.id} for item in fragment.items.all()]
            response["orders"].append(data)
        return Response(response, status=status.HTTP_200_OK)


class ShowOTP(APIView):

    permission_classes = (IsAuthenticated, TokenVerification,)

    acceptable_status = ["R", "F"]

    def post(self, request):
        try:
            order_id = request.data['order_id']
            stall_id = request.data['stall_id']
        except KeyError as e:
            msg = {"message" : "The following field was missing: {}".format(e)}
            return Response(msg, status = status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(pk = order_id)
            stall = Stall.objects.get(pk = stall_id)
            order_frag = order.fragments.get(stall = stall)
        except:
            msg = {"message" : "Either the Order or the Stall doesn't exist."}
            return Response(msg, status = status.HTTP_404_NOT_FOUND)

        if not order_frag.status in self.acceptable_status:
            msg = {"message" : "Cannot view  the order status"}
            return Response(msg, status = status.HTTP_400_BAD_REQUEST)

        order_frag.show_otp = True
        order_frag.save()

        return Response(status = status.HTTP_200_OK)


########## Prof Show Stuff: ##########

class GetTickets(APIView):

    permission_classes = (TokenVerification,)

    @csrf_exempt
    def post(self, request):
        qr_code = request.data["qr_code"]
        # user_id = decString(qr_code)[0]        # a custom function from utils.wallet_qrcode
        # user = get_object_or_404(User, id=user_id)
        try:
            user = Wallet.objects.get(uuid=qr_code).user
        except Exception as e:
            print(e)
            return Response({"message": "user does not exist."}, status=status.HTTP_404_NOT_FOUND)


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
                "qr_code": "a8a2c8c8-d8ba-432f-ba67-fc946cf0536a",
                "consume": 3,
                "show_id": 1
           }
    """

    permission_classes = (TokenVerification, IsAuthenticated,)

    @csrf_exempt
    def post(self, request):

        try:
            organization = request.user.organization # note: model found in the events app
            name = organization.name
            if organization.disabled:
                raise Organization.DoesNotExist
        except Organization.DoesNotExist:
            return Response({"message": "User is not an organization (club/dept)."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            try:
                qr_code = request.data["qr_code"]
                #user_id = int(decString(qr_code)[0])
            except:
                return Response({"message": "invalid qr_code"}, status=status.HTTP_404_NOT_FOUND)

            #user = get_object_or_404(User, id=user_id)
            try:
                wallet = get_object_or_404(Wallet, uuid=qr_code)
            except:
                return Response({"message": "invalid qr_code"}, status=status.HTTP_404_NOT_FOUND)
            user = wallet.user
            show = get_object_or_404(MainProfShow, id=request.data["show_id"])

            try:
                tickets = Tickets.objects.get(user=user, prof_show=show)
                if tickets == None:
                    raise Tickets.DoesNotExist
            except:
                return Response({"success": False, "max_tickets": 0, "x-status": 2}) # the scanee has never bought tickets for this show before

            if show not in organization.shows.all():
                return Response({"message": "Invalid user, only members of {} are allowed to control tickets for this show.".format(show.organizations.all())}, status=status.HTTP_401_UNAUTHORIZED)

            consume = request.data["consume"]

            max_count = tickets.count
            if(consume > max_count):
                if any([tickets.consumed > 0, tickets.count > 0]):
                    return Response({"success": False, "max_tickets": max_count, "x-status": 1})
                return Response({"success": False, "max_tickets": max_count, "x-status": 2}) # the scanee has never bought tickets for this show before
            if consume < 1:
                return Response({"success": False, "message": "Number of tickets can't be less than 1", "max_tickets": max_count, "x-status": -1})
            tickets.count -= consume
            tickets.consumed += consume
            tickets.save()

            TicketTransaction.objects.create(tickets=tickets, num=consume)

            return Response({"success": True, "remaining_tickets": tickets.count, "x-status": 0})

        except KeyError as ke:
            return Response({"success": False, "message": "missing field: {}".format(ke)}, status=status.HTTP_400_BAD_REQUEST)


class N2OTickets(APIView):

    permission_classes = (IsAuthenticated, TokenVerification)

    def get(self, request):
        try:
            organization = request.user.organization
            name = organization.name
            if organization.disabled:
                raise Organization.DoesNotExist
        except Organization.DoesNotExist:
            return Response({"message": "Restricted Access."}, status=status.HTTP_401_UNAUTHORIZED)

        if not name == "has":
            msg = {"message" : "Unauthorized Access. Only HAS is allowed."}
            return Response(msg, status=status.HTTP_401_UNAUTHORIZED)

        try:
            prof_show = MainProfShow.objects.get(name="N2O")
            if prof_show == None:
                raise MainProfShow.DoesNotExist
        except MainProfShow.DoesNotExist:
            msg = {"message": "Prof Show does not exist."}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

        count = 0
        tickets = prof_show.tickets.all()
        for ticket in tickets:
            count += ticket.count

        resp = {"count" : count}
        return Response(resp, status=status.HTTP_200_OK)


    def post(self, request):
        ticket_count = 0
        try:
            organization = request.user.organization
            name = organization.name
            if organization.disabled:
                raise Organization.DoesNotExist
        except Organization.DoesNotExist:
            return Response({"message": "Restricted Access."}, status=status.HTTP_401_UNAUTHORIZED)

        if not name == "has":
            msg = {"message" : "Unauthorized Access. Only HAS is allowed."}
            return Response(msg, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        try:
            qr_code = data["qr_code"]
            ticket_count = data["ticket_count"]
        except KeyError as missing:
            msg = {"message" : "The following field was missing: {}".format(missing)}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Wallet.objects.get(uuid=qr_code).user
        except User.DoesNotExist:
            msg = {"message": "User doesn't exist."}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        except Wallet.DoesNotExist:
            msg = {"message": "Invalid qr_code."}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        except:
            msg = {"message" : "Badly formed uuid."}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        try:
            prof_show = MainProfShow.objects.get(name="N2O")
            if prof_show == None:
                raise MainProfShow.DoesNotExist
        except MainProfShow.DoesNotExist:
            msg = {"message": "Prof Show does not exist."}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

        tickets, _ = Tickets.objects.get_or_create(prof_show=prof_show, user=user)
        tickets.count += ticket_count
        tickets.save()

        msg = {"message" : "Request Successful!"}
        return Response(msg, status=status.HTTP_200_OK)


class RefundTickets(APIView):
    """
        This endpoint was made after the fest for refunding prof show tickets after
        requesting the CRC to do so. It is not a main part of the codebase.
            {
                "qr_code": "a8a2c8c8-d8ba-432f-ba67-fc946cf0536a",
            }
    """

    permission_classes = (TokenVerification, IsAuthenticated,)

    @csrf_exempt
    def post(self, request):
        try:
            if request.user.username != "crc":
                return Response({"message": "Only the CRC is allowed to perform this action. Please sign in with the CRC's account."}, status=403)
            qr_code = request.data["qr_code"]
            try:
                refund_user = Wallet.objects.get(uuid=qr_code).user.bitsian
            except:
                return Response({"message": "invalid QR code, no such Bitsian"}, status=404)
            if not refund_user.wants_refund:
                refund_user.wants_refund = True
                refund_user.save(update_fields=['wants_refund'])
                return Response({"message": "Successful!"}, status=200)
            return Response({"message": "Already done!"}, status=200)
        except KeyError as key:
            return Response({"message": "missing key: {}".format(key)}, status=400)

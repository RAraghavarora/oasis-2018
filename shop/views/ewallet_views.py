from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from shop.models.wallet import Wallet
from shop.permissions import TokenVerification

import json, requests
from instamojo_wrapper import Instamojo
from rest_framework.reverse import reverse

from oasis2018.settings_config.keyconfig import *

from registrations.models import Participant,Bitsian
from django.contrib.auth.models import User
from shop.models.transaction import Transaction
from firebase_admin import firestore
from rest_framework.renderers import TemplateHTMLRenderer


try:
    if SERVER:
        raise
    api = Instamojo(api_key=INSTA_API_KEY, auth_token=AUTH_TOKEN)
except:
    api = Instamojo(api_key=INSTA_API_KEY_test, auth_token=AUTH_TOKEN_test, endpoint='https://test.instamojo.com/api/1.1/') #when in development


class Transfer(APIView):
    """
        The API endpoint that will be called when money is to be transferred
        from one user's wallet to another. This view may even be called by other
        views such as the PlaceOrder view to abstract the process of
        transferring money.
    """

    permission_classes = (IsAuthenticated, TokenVerification,)

    def post(self, request, format=None):
            data = request.data
            try:
                source = request.user.wallet
                target_user = User.objects.get(id=data["target_user"])
                target = Wallet.objects.get(user=target_user)
                if source == target:
                    return Response({"message": "You can't transfer money to yourself."}, status=status.HTTP_403_FORBIDDEN)
                amount = data["amount"]
                if amount < 0:
                    return Response({"message": "transfered amount cannot be negative."}, status=status.HTTP_400_BAD_REQUEST)
                source.transferTo(target, amount, transfertype="transfer")
                msg = {"message": "successful!"}
                return Response(msg, status=status.HTTP_200_OK)
            except KeyError as missing:
                msg = {"message": "missing the following field: {}".format(missing)}
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            except Wallet.DoesNotExist:
                msg = {"message": "Wallet does not exist"}
                return Response(msg, status=status.HTTP_404_NOT_FOUND)


def changeActiveTransfer(open_modal, success, user):
        """ Modify some user data in firebase to allow the app to
        know if the payment was successful or not and if it should
        close the modal/window pop up for payment. Have the app and/or
        frontend people make sure that they set "success" to false
        after they have seen that it was successful. """

        db = firestore.client()
        data = {"open_modal": open_modal, "success": success}
        db.collection("User #{}".format(user.id)).document("Active Transfer").set(data)


class AddMoney(APIView):
    """
        The API endpoint that will be called when money has to be added to
        the wallet by Credit/Debit Cards or UPIs via Instamojo.
    """

    permission_classes= (IsAuthenticated, TokenVerification,)

    def post(self, request, format=None):
        data = request.data

        try:
            origin = request.META["HTTP_X_ORIGIN"]
            if origin not in ["iOS", "Web", "Android"]:
                return Response({"message": "invalid x-origin"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"message": "x-origin missing from headers."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount=data['amount']
            if amount<0:
                return Response({"message": "Amount to be added cannot be negative."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                profile = Participant.objects.get(user=request.user)
            except:
                try:
                    profile = Bitsian.objects.get(user=request.user)
                except:
                    return Response({"message": "The user has not been identified as a bitsian nor as participant."}, status=status.HTTP_403_FORBIDDEN)
            user_email = profile.email
            user_mobile = profile.phone
            user_name = profile.name

            # just check if the wallet exists before continuing
            try:
                wallet = profile.user.wallet
            except:
                return Response({"message": "The user has no wallet. Cannot add money as of yet."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            if origin == "iOS":
                redirect_url = reverse("shop:AddMoneyResponseIOS",request=request)
            elif origin == "Web":
                redirect_url = reverse("shop:AddMoneyResponseWeb",request=request)
            elif origin == "Android":
                redirect_url = reverse("shop:AddMoneyResponseAndroid",request=request)
            # print("Hi")
            response = api.payment_request_create(
                amount=str(amount),
                purpose='Add Money to wallet',
                send_email=False,
                email=user_email,
                buyer_name=user_name,
                phone=user_mobile,
                redirect_url=redirect_url
            )
            # print("Hi")
            # print(response)

            changeActiveTransfer(True, False, request.user)
            # print("Hi")

            return Response({'url': response['payment_request']['longurl']})
        except Exception as e:
            print("ADD MONEY FAILED!!!")
            print(e)
            return Response({'message': 'Add Money Failed! '})
            


def AddMoneyResponse(request):
    '''
        A function called by the AddMoneyResponse____ views
    '''

    data = request.GET
    # print(data)
    # print(request.META)

    try:
        payid = data['payment_request_id']
        # print(payid)
        changeActiveTransfer(False, False, request.user)
    except Exception as e:
        return Response({'message': 'missing key in body "payment_request_id"'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        headers = {'X-Api-Key': INSTA_API_KEY, 'X-Auth-Token': AUTH_TOKEN}
        r = requests.get('https://www.instamojo.com/api/1.1/payment-requests/'+str(payid),headers=headers)
    except:
        headers = {'X-Api-Key': INSTA_API_KEY_test, 'X-Auth-Token': AUTH_TOKEN_test}
        r = requests.get('https://test.instamojo.com/api/1.1/payment-requests/'+str(payid), headers=headers)

    json_ob=r.json()
    # print(json_ob)
    status_ = json_ob['success']
    # print(status_)

    if not status_:
        changeActiveTransfer(False, False, request.user)
        return Response({'message': 'Payment not successful/cancelled. '}, status=status.HTTP_200_OK)

    else:
        # print("HEYYYYYYYYYYYY")
        payment_id=json_ob['payment_request']['payments'][0]['payment_id']
        try:
            profile = Participant.objects.get(email=json_ob['payment_request']['email'])
            user_ = profile.user
        except:
            try:
                profile = Bitsian.objects.get(email=json_ob['payment_request']['email'])
                user_ = profile.user 
            except:
                changeActiveTransfer(False, False, request.user)
                return Response({"message": "The user has not been identified as a bitsian nor as participant."}, status=status.HTTP_403_FORBIDDEN)

        wallet = Wallet.objects.get(user=user_)
        amount = int(float(json_ob['payment_request']['amount']))
        try:
            transaction = Transaction(
                amount=amount, transfer_from=wallet, transfer_to=wallet,transfer_type="add", payment_id=payment_id)
            transaction.save()
        except Exception as e:
            changeActiveTransfer(False, False, request.user)
            return Response({'message': "You have encashed this money. "}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        wallet.balance.add(0,0,amount,0)
        # print("ADDED {}".format(amount))

        changeActiveTransfer(False, True, request.user)
        return "OK"
        # print("EOC")


class AddMoneyResponseWeb(APIView):

    def get(self, request, format=None):
        resp = AddMoneyResponse(request)
        if not resp == "OK":
            return resp
        return Response({"message": "Hello Laksh/Kunal! Wassup? DO SOMETHING WEB, payment successful"})


class AddMoneyResponseIOS(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shop/base.html'

    def get(self, request, format=None):
        resp = AddMoneyResponse(request)
        if not resp == "OK":
            return resp
        return Response({"message": "Hello Sarthak!! Wassup? DO SOMETHING iOS, payment successful"})


class AddMoneyResponseAndroid(APIView):

    def get(self, request, format=None):
        resp = AddMoneyResponse(request)

        if not resp == 'OK':
            return resp

        return Response({"message": "DO SOMETHING ANDROID, payment successful"})

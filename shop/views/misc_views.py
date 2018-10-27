from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required,user_passes_test

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from shop.permissions import TokenVerification
from shop.models.debug import DebugInfo
from registrations.models import Bitsian
from events.models import MainProfShow
from events.serializers import MainProfShowSerializer
from shop.models.wallet import Wallet
from shop.models.transaction import Transaction

class GetProfile(APIView):

    permission_classes = (IsAuthenticated, TokenVerification,)

    @csrf_exempt
    def get(self, request):
        user = request.user
        try:
            profile = user.bitsian
        except:
            try:
                profile = user.participant
            except:
                return Response({"message": "The user is neither a bitsian nor a participant nor a stall. Hence has no profile"}, status=status.HTTP_404_NOT_FOUND)

        response_data = dict()
        response_data["name"] = profile.name
        response_data["balance"] = user.wallet.getTotalBalance()
        response_data["qr_code"] = user.wallet.uuid
        if isinstance(profile, Bitsian):
            response_data["bits-id"] = profile.long_id
            response_data["college"] = "BITS Pilani"
        else:
            if profile.college:
                response_data["college"] = str(profile.college)
            else:
                response_data["college"] = ""
            response_data["bits-id"] = None
        return Response(response_data, status=status.HTTP_200_OK)


class GetProfShows(APIView):

        permission_classes = (TokenVerification,)

        @csrf_exempt
        def get(self, request):
            shows = list()
            for show in MainProfShow.objects.all():
                shows.append(MainProfShowSerializer(show).data)
            return Response({"shows": shows})


class AppDebugInfo(APIView):

    permission_classes = (TokenVerification,)

    identity_dict = {long_form : short_form for short_form, long_form in DebugInfo.IDENTITY}

    def post(self, request):
        try:
            debug_info = request.data["debug_info"]
            identity = request.data["identity"].title()
        except KeyError as missing:
            msg = {"message" : "The following field was missing: {}".format(missing)}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        try:
            identity = self.identity_dict[identity]
        except KeyError:
            msg = {"message" : "Wrong Identity."}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        DebugInfo.objects.create(identity=identity, debug_info=debug_info)

        msg = {"message" : "Request Successful."}
        return Response(msg, status=status.HTTP_200_OK)


@user_passes_test(lambda x: x.is_superuser)
def viewTransactions(request, uuid):
    wallet = Wallet.objects.get(uuid=uuid)
    context = {}
    context["transactions_in"] = Transaction.objects.filter(transfer_to=wallet)
    context["transactions_out"] = Transaction.objects.filter(transfer_from=wallet)
    try:
        context["name"] = wallet.user.participant.name
    except:
        context["name"] = wallet.user.bitsian.name
    return render(request, "shop/transactions.html", context)

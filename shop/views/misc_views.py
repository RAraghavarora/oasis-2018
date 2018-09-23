from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from shop.permissions import TokenVerification
from registrations.models import Bitsian


class GetProfile(APIView):

    permission_classes = (IsAuthenticated, TokenVerification)

    @csrf_exempt
    def post(self, request):
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
        response_data["qr_code"] = profile.barcode # @Juniors: please name it qr_code and not barcode.... we would have but it's a bit late.
        if isinstance(profile, Bitsian):
            response_data["bits-id"] = profile.long_id
        else:
            response_data["bits-id"] = None
        return Response(response_data, status=status.HTTP_200_OK)

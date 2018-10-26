from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from shop.models.debug import DebugInfo
from shop.permissions import TokenVerification
from shop.models.debug import DebugInfo
from registrations.models import Bitsian
from events.models import MainProfShow
from events.serializers import MainProfShowSerializer


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
        response_data["qr_code"] = profile.barcode # @Juniors: please name it qr_code and not barcode.... we would have but it was a bit too late.
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

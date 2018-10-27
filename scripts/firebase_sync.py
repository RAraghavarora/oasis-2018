import os
import firebase_admin
from firebase_admin import credentials
from django.conf import settings

from event.models import Participant
from shop.models.wallet import Wallet


class Syncer:

    def __init__(self):
        try:
            # initialize the Firebase Admin SDK.
            path = "oasis2018/settings_config/firebase_creds.json"
            creds = credentials.Certificate(os.path.join(
                                                settings.BASE_DIR,
                                                path
                                                )
                                            )
            app = firebase_admin.initialize_app(creds)
        except:
            # the Firebase Admin SDK has already been initiaized by the app.
            pass

    def sync_participants_wallets(self):
        all_participants = Participant.objects.all()
        for participant in all_participants:
            print("processing #%d - %s" % (participant.id, participant.name))
            if participant.firewallz_passed:
                wallet, created = Wallet.objects.get_or_create(user=participant.user, profile="P")
                if created:
                    balance = Balance.objects.create(wallet=wallet)
                    wallet.balance = balance
                    wallet.save()
                    balance.save()

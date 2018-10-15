import os

from django.apps import AppConfig
from django.conf import settings

import firebase_admin
from firebase_admin import credentials


class ShopConfig(AppConfig):
    name = 'shop'

    def ready(self):
        """ Get the application ready. """
        # First, import all signals.
        from shop.signals.balance import balanceFirebaseUpdate # obviously realtime is required
        from shop.signals.balance import balanceFirebaseDelete
        from shop.signals.item import itemClassFirebaseUpdate # for availability, realtime on firebase
        from shop.signals.item import itemClassFirebaseDelete
        from shop.signals.order import orderFragmentFirebaseUpdate # for status, realtime on firebase
        from shop.signals.order import orderFragmentFirebaseDelete
        from shop.signals.instawallet import autoAddWalletStall # for adding a wallet to stalls
        from shop.signals.instawallet import autoAddWalletBitsian # for adding a wallet to bitsians
        from shop.signals.instawallet import autoAddWalletParticipant # for adding a wallet to bitsians

        #Then use Google's API to get setup for communtication with
        #Google Cloud Firestore from the server end.
        try:
            path = "oasis2018/settings_config/firebase_creds.json"
            creds = credentials.Certificate(os.path.join(
                                                settings.BASE_DIR,
                                                path
                                                )
                                            )
            app = firebase_admin.initialize_app(creds)
        except:
            pass # already initialized by another app

"""
For learning more about how to use Google Cloud Firestore's api,
https://firebase.google.com/docs/firestore/data-model#collections
https://github.com/firebase/firebase-admin-python
https://github.com/GoogleCloudPlatform/google-cloud-python
https://googlecloudplatform.github.io/google-cloud-python/latest/firestore/client.html
"""

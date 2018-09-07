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
        from shop.signals.balance import balanceFirebaseUpdate
        from shop.signals.balance import balanceFirebaseDelete
        from shop.signals.item import itemClassFirebaseUpdate
        from shop.signals.item import itemClassFirebaseDelete
        from shop.signals.order import orderFragmentFirebaseUpdate
        from shop.signals.order import orderFragmentFirebaseDelete
        from shop.signals.transaction import transactionFirebaseDelete
        from shop.signals.transaction import transactionFirebaseUpdate
        from shop.signals.wallet import walletFirebaseUpdate
        from shop.signals.wallet import walletFirebaseDelete

        # Then use Google's API to get setup for communtication with
        # Google Cloud Firestore from the server end.
        creds = credentials.Certificate(os.path.join(
                                                settings.BASE_DIR,
                                                "oasis2018/firebase_creds.json"
                                                )
                                        )
        app = firebase_admin.initialize_app(creds)


"""
For learning more about how to use Google Cloud Firestore's api,
https://firebase.google.com/docs/firestore/data-model#collections
https://github.com/firebase/firebase-admin-python
https://github.com/GoogleCloudPlatform/google-cloud-python
https://googlecloudplatform.github.io/google-cloud-python/latest/firestore/client.html
"""

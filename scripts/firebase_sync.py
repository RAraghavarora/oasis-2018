import os
import firebase_admin
from firebase_admin import credentials
from django.conf import settings


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

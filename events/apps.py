import os

from django.apps import AppConfig
from django.conf import settings

import firebase_admin
from firebase_admin import credentials


class EventsConfig(AppConfig):
    name = 'events'

    def ready(self):
        """ Get the application ready. """
        # First, import all signals.
        from events.signals import mainEventsRealtimeUpdate, mainEventsRealtimeDelete

        #Then use Google's API to get setup for communtication with
        #Google Cloud Firestore from the server end.
        path = "oasis2018/settings_config/firebase_creds.json"
        creds = credentials.Certificate(os.path.join(
                                            settings.BASE_DIR,
                                            path
                                            )
                                        )
        app = firebase_admin.initialize_app(creds)


        # look at the signals in the wallet app for more.

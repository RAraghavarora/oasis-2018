from django.conf import settings

import firebase_admin
from firebase_admin import credentials, firestore

def getFirestoreDatabase():
    """
        Use Google's API to get setup for communtication with Google Cloud
        Firestore from the server end. The returned object can be used to
        directly communicate with the Cloud Firestore database.
    """
    creds = credentials.Certificate(os.path.join(
                                            BASE_DIR,
                                            "oasis2018/firebase_creds.json"
                                            )
                                    )
    app = firebase_admin.initialize_app(creds)
    return firestore.client()

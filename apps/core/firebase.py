import firebase_admin
from firebase_admin import credentials, firestore, auth
from django.conf import settings
import os
import json
import base64


class FirebaseService:
    """Singleton Firebase service — initializes once, reuses everywhere."""

    _instance = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._initialize()
        return cls._instance

    @classmethod
    def _initialize(cls):
        """Initialize Firebase Admin SDK.

        Supports two modes:
          1. FIREBASE_CREDENTIALS_BASE64 env var (cloud deployments)
          2. FIREBASE_CREDENTIAL_PATH file path (local development)
        """
        if not firebase_admin._apps:
            b64 = os.getenv('FIREBASE_CREDENTIALS_BASE64', '')
            if b64:
                # Decode base64 → JSON dict → Certificate
                cred_dict = json.loads(base64.b64decode(b64))
                cred = credentials.Certificate(cred_dict)
            else:
                # Fall back to file path
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIAL_PATH)
            firebase_admin.initialize_app(cred)
        cls._db = firestore.client()

    @property
    def db(self):
        """Return Firestore client."""
        return self._db

    @staticmethod
    def verify_token(id_token):
        """Verify a Firebase ID token and return decoded claims."""
        try:
            decoded = auth.verify_id_token(id_token)
            return decoded
        except Exception:
            return None


# Module-level convenience functions
def get_firestore_client():
    """Get the Firestore client instance."""
    return FirebaseService().db


def verify_firebase_token(id_token):
    """Verify a Firebase ID token."""
    return FirebaseService.verify_token(id_token)

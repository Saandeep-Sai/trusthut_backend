from datetime import datetime
from apps.core.firebase import get_firestore_client
from apps.core.config import USERS_COLLECTION


def create_user(uid, name, email):
    """Create a new user document in Firestore."""
    db = get_firestore_client()
    user_data = {
        'uid': uid,
        'name': name,
        'email': email,
        'created_at': datetime.utcnow().isoformat(),
    }
    db.collection(USERS_COLLECTION).document(uid).set(user_data)
    return user_data


def get_user(uid):
    """Get a user document from Firestore."""
    db = get_firestore_client()
    doc = db.collection(USERS_COLLECTION).document(uid).get()
    if doc.exists:
        return doc.to_dict()
    return None


def update_user(uid, data):
    """Update a user document in Firestore."""
    db = get_firestore_client()
    db.collection(USERS_COLLECTION).document(uid).update(data)
    updated_doc = db.collection(USERS_COLLECTION).document(uid).get()
    return updated_doc.to_dict()


def get_all_users():
    """Get all user documents from Firestore."""
    db = get_firestore_client()
    docs = db.collection(USERS_COLLECTION).stream()
    users = []
    for doc in docs:
        users.append(doc.to_dict())
    users.sort(key=lambda u: u.get('created_at', ''), reverse=True)
    return users

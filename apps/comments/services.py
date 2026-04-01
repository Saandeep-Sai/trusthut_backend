import uuid
from datetime import datetime
from apps.core.firebase import get_firestore_client
from apps.core.config import COMMENTS_COLLECTION, USERS_COLLECTION


def add_comment(user_id, post_id, text):
    """Add a comment to a post."""
    db = get_firestore_client()
    comment_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    # Look up user name
    user_doc = db.collection(USERS_COLLECTION).document(user_id).get()
    user_name = user_doc.to_dict().get('name', 'User') if user_doc.exists else 'User'

    comment_data = {
        'comment_id': comment_id,
        'post_id': post_id,
        'user_id': user_id,
        'user_name': user_name,
        'text': text,
        'created_at': now,
    }

    db.collection(COMMENTS_COLLECTION).document(comment_id).set(comment_data)
    return comment_data


def get_comments(post_id):
    """Get all comments for a post, sorted oldest first."""
    db = get_firestore_client()
    docs = db.collection(COMMENTS_COLLECTION).where(
        'post_id', '==', post_id
    ).stream()
    comments = [doc.to_dict() for doc in docs]
    comments.sort(key=lambda c: c.get('created_at', ''))
    return comments


def delete_comment(comment_id, user_id):
    """Delete a comment (owner only). Returns True if deleted."""
    db = get_firestore_client()
    doc = db.collection(COMMENTS_COLLECTION).document(comment_id).get()
    if not doc.exists:
        return False
    data = doc.to_dict()
    if data.get('user_id') != user_id:
        return False
    db.collection(COMMENTS_COLLECTION).document(comment_id).delete()
    return True


def get_comment_count(post_id):
    """Get the number of comments for a post."""
    db = get_firestore_client()
    docs = db.collection(COMMENTS_COLLECTION).where(
        'post_id', '==', post_id
    ).stream()
    return sum(1 for _ in docs)

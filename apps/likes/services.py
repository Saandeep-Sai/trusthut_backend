import uuid
from apps.core.firebase import get_firestore_client
from apps.core.config import LIKES_COLLECTION, POSTS_COLLECTION


def like_post(user_id, post_id):
    """Like a post. Returns True if new like, False if already liked."""
    db = get_firestore_client()

    # Check if already liked
    existing = db.collection(LIKES_COLLECTION).where(
        'user_id', '==', user_id
    ).where(
        'post_id', '==', post_id
    ).get()

    if len(existing) > 0:
        return False

    # Create like document
    like_id = str(uuid.uuid4())
    db.collection(LIKES_COLLECTION).document(like_id).set({
        'like_id': like_id,
        'user_id': user_id,
        'post_id': post_id,
    })

    # Increment likes_count on the post
    post_ref = db.collection(POSTS_COLLECTION).document(post_id)
    post = post_ref.get()
    if post.exists:
        current_count = post.to_dict().get('likes_count', 0)
        post_ref.update({'likes_count': current_count + 1})

    return True


def unlike_post(user_id, post_id):
    """Unlike a post. Returns True if removed, False if not found."""
    db = get_firestore_client()

    existing = db.collection(LIKES_COLLECTION).where(
        'user_id', '==', user_id
    ).where(
        'post_id', '==', post_id
    ).get()

    if len(existing) == 0:
        return False

    # Delete like document
    for doc in existing:
        db.collection(LIKES_COLLECTION).document(doc.id).delete()

    # Decrement likes_count on the post
    post_ref = db.collection(POSTS_COLLECTION).document(post_id)
    post = post_ref.get()
    if post.exists:
        current_count = post.to_dict().get('likes_count', 0)
        post_ref.update({'likes_count': max(0, current_count - 1)})

    return True


def has_user_liked(user_id, post_id):
    """Check if a user has liked a post."""
    db = get_firestore_client()
    existing = db.collection(LIKES_COLLECTION).where(
        'user_id', '==', user_id
    ).where(
        'post_id', '==', post_id
    ).get()
    return len(existing) > 0

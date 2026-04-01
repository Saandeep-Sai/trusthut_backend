import uuid
from datetime import datetime
from apps.core.firebase import get_firestore_client
from apps.core.config import POSTS_COLLECTION


def create_post(user_id, validated_data):
    """Create a new post in Firestore."""
    db = get_firestore_client()
    post_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    # Look up the user's name to store with the post
    from apps.core.config import USERS_COLLECTION
    user_doc = db.collection(USERS_COLLECTION).document(user_id).get()
    user_name = user_doc.to_dict().get('name', 'User') if user_doc.exists else 'User'

    post_data = {
        'post_id': post_id,
        'user_id': user_id,
        'user_name': user_name,
        'title': validated_data['title'],
        'description': validated_data['description'],
        'location_name': validated_data['location_name'],
        'latitude': validated_data['latitude'],
        'longitude': validated_data['longitude'],
        'accessibility_type': validated_data['accessibility_type'],
        'risk_level': validated_data['risk_level'],
        'media_url': validated_data.get('media_url', ''),
        'media_type': validated_data.get('media_type', 'image'),
        # Highway safety fields (backward-compatible defaults)
        'post_type': validated_data.get('post_type', 'place'),
        'risk_category': validated_data.get('risk_category', ''),
        'route_name': validated_data.get('route_name', ''),
        'likes_count': 0,
        'created_at': now,
        'updated_at': now,
    }

    db.collection(POSTS_COLLECTION).document(post_id).set(post_data)
    return post_data


def get_all_posts():
    """Get all posts ordered by creation date."""
    db = get_firestore_client()
    docs = db.collection(POSTS_COLLECTION).order_by(
        'created_at', direction='DESCENDING'
    ).stream()
    return [doc.to_dict() for doc in docs]


def get_post(post_id):
    """Get a single post by ID."""
    db = get_firestore_client()
    doc = db.collection(POSTS_COLLECTION).document(post_id).get()
    if doc.exists:
        return doc.to_dict()
    return None


def update_post(post_id, validated_data):
    """Update a post in Firestore."""
    db = get_firestore_client()
    validated_data['updated_at'] = datetime.utcnow().isoformat()
    db.collection(POSTS_COLLECTION).document(post_id).update(validated_data)
    return get_post(post_id)


def delete_post(post_id):
    """Delete a post from Firestore."""
    db = get_firestore_client()
    db.collection(POSTS_COLLECTION).document(post_id).delete()


def search_posts(query):
    """Search posts by keyword in title, description, and location_name."""
    db = get_firestore_client()
    all_docs = db.collection(POSTS_COLLECTION).stream()
    query_lower = query.lower()

    results = []
    for doc in all_docs:
        data = doc.to_dict()
        searchable = f"{data.get('title', '')} {data.get('description', '')} {data.get('location_name', '')}".lower()
        if query_lower in searchable:
            results.append(data)

    return results


def get_user_posts(user_id):
    """Get all posts by a specific user."""
    db = get_firestore_client()
    docs = db.collection(POSTS_COLLECTION).where(
        'user_id', '==', user_id
    ).stream()
    posts = [doc.to_dict() for doc in docs]
    posts.sort(key=lambda p: p.get('created_at', ''), reverse=True)
    return posts


def get_highway_risks(risk_category=None, severity=None):
    """Get all highway risk posts, optionally filtered."""
    db = get_firestore_client()
    query = db.collection(POSTS_COLLECTION).where('post_type', '==', 'highway')
    docs = query.stream()

    results = []
    for doc in docs:
        data = doc.to_dict()
        # Apply optional filters in Python (avoids composite index requirement)
        if risk_category and data.get('risk_category') != risk_category:
            continue
        if severity and data.get('risk_level') != severity:
            continue
        results.append(data)

    results.sort(key=lambda p: p.get('created_at', ''), reverse=True)
    return results

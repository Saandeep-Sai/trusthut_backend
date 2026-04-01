import math
from apps.core.firebase import get_firestore_client
from apps.core.config import POSTS_COLLECTION


def decode_polyline(encoded):
    """Decode a Google Maps encoded polyline into a list of (lat, lng) tuples."""
    points = []
    index = 0
    lat = 0
    lng = 0
    while index < len(encoded):
        # Latitude
        shift = 0
        result = 0
        while True:
            b = ord(encoded[index]) - 63
            index += 1
            result |= (b & 0x1F) << shift
            shift += 5
            if b < 0x20:
                break
        dlat = ~(result >> 1) if (result & 1) else (result >> 1)
        lat += dlat

        # Longitude
        shift = 0
        result = 0
        while True:
            b = ord(encoded[index]) - 63
            index += 1
            result |= (b & 0x1F) << shift
            shift += 5
            if b < 0x20:
                break
        dlng = ~(result >> 1) if (result & 1) else (result >> 1)
        lng += dlng

        points.append((lat / 1e5, lng / 1e5))

    return points


def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance in meters between two lat/lng points."""
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def sample_waypoints(points, interval=20):
    """Sample every Nth point from a polyline to reduce computation."""
    if len(points) <= interval:
        return points
    return points[::interval] + [points[-1]]


def score_route(waypoints, all_posts, radius_m=500):
    """Score a route based on nearby TrustHut reports.

    Risk weights: unsafe=5, moderate=3, safe=1
    Lower score = safer route.
    """
    WEIGHTS = {'unsafe': 5, 'moderate': 3, 'safe': 1}
    high_count = 0
    moderate_count = 0
    low_count = 0
    nearby_posts = []
    seen_ids = set()

    for wp_lat, wp_lng in waypoints:
        for post in all_posts:
            pid = post.get('post_id')
            if pid in seen_ids:
                continue
            plat = post.get('latitude', 0)
            plng = post.get('longitude', 0)
            dist = haversine(wp_lat, wp_lng, plat, plng)
            if dist <= radius_m:
                seen_ids.add(pid)
                risk = post.get('risk_level', 'safe').lower()
                if risk == 'unsafe':
                    high_count += 1
                elif risk == 'moderate':
                    moderate_count += 1
                else:
                    low_count += 1
                nearby_posts.append({
                    'post_id': pid,
                    'title': post.get('title', ''),
                    'risk_level': post.get('risk_level', ''),
                    'risk_category': post.get('risk_category', ''),
                    'location_name': post.get('location_name', ''),
                    'latitude': plat,
                    'longitude': plng,
                    'distance_m': round(dist),
                })

    total_score = (high_count * WEIGHTS['unsafe']
                   + moderate_count * WEIGHTS['moderate']
                   + low_count * WEIGHTS['safe'])

    # Safety rating label
    if total_score == 0:
        rating = 'Very Safe'
    elif total_score <= 5:
        rating = 'Safe'
    elif total_score <= 15:
        rating = 'Moderate'
    elif total_score <= 30:
        rating = 'Risky'
    else:
        rating = 'Dangerous'

    return {
        'risk_score': total_score,
        'safety_rating': rating,
        'high_risk_count': high_count,
        'moderate_risk_count': moderate_count,
        'low_risk_count': low_count,
        'nearby_reports': nearby_posts[:10],  # Limit to top 10
    }


def get_all_posts_for_scoring():
    """Fetch all posts from Firestore for route scoring."""
    db = get_firestore_client()
    docs = db.collection(POSTS_COLLECTION).stream()
    return [doc.to_dict() for doc in docs]

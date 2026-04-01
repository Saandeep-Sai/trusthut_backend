# Centralized configuration constants for TrustHut

# Firestore collection names
USERS_COLLECTION = 'users'
POSTS_COLLECTION = 'posts'
LIKES_COLLECTION = 'likes'
COMMENTS_COLLECTION = 'comments'

# Valid field values
ACCESSIBILITY_TYPES = ['wheelchair', 'elder', 'general']
RISK_LEVELS = ['safe', 'moderate', 'unsafe']

# Post types (backward-compatible — existing posts default to 'place')
POST_TYPES = ['place', 'highway']

# Highway risk categories
RISK_CATEGORIES = ['accident', 'sharp_turn', 'bad_road', 'no_lighting', 'congestion']

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

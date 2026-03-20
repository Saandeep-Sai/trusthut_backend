from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.users.middleware import firebase_auth_required
from apps.users import services


@api_view(['POST'])
@firebase_auth_required
def register_user(request):
    """Register a new user after Firebase auth signup."""
    uid = request.firebase_uid
    name = request.data.get('name', '')
    email = request.data.get('email', '')

    if not name or not email:
        return Response(
            {'status': 'error', 'message': 'Name and email are required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if user already exists
    existing = services.get_user(uid)
    if existing:
        return Response(
            {'status': 'error', 'message': 'User already registered.'},
            status=status.HTTP_409_CONFLICT,
        )

    user_data = services.create_user(uid, name, email)
    return Response(
        {'status': 'success', 'message': 'User registered.', 'data': user_data},
        status=status.HTTP_201_CREATED,
    )


@api_view(['GET', 'PUT'])
@firebase_auth_required
def profile(request):
    """Get or update user profile."""
    uid = request.firebase_uid

    if request.method == 'GET':
        user = services.get_user(uid)
        if not user:
            # Auto-create profile from Firebase Auth data
            try:
                from firebase_admin import auth as fb_auth
                fb_user = fb_auth.get_user(uid)
                email = fb_user.email or ''
                name = fb_user.display_name or email.split('@')[0] or 'User'
            except Exception:
                email = ''
                name = 'User'
            user = services.create_user(uid, name, email)
        return Response({'status': 'success', 'data': user})

    # PUT — update profile
    allowed_fields = {'name'}
    update_data = {k: v for k, v in request.data.items() if k in allowed_fields}

    if not update_data:
        return Response(
            {'status': 'error', 'message': 'No valid fields to update.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    updated = services.update_user(uid, update_data)
    return Response({'status': 'success', 'data': updated})

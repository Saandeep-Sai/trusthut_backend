from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from apps.core.firebase import verify_firebase_token


def firebase_auth_required(view_func):
    """Decorator that verifies Firebase ID token from Authorization header.

    On success, attaches `request.firebase_uid` for downstream use.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header.startswith('Bearer '):
            return Response(
                {'status': 'error', 'message': 'Authorization header missing or invalid.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = auth_header.split('Bearer ')[1]
        decoded = verify_firebase_token(token)

        if decoded is None:
            return Response(
                {'status': 'error', 'message': 'Invalid or expired token.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        request.firebase_uid = decoded['uid']
        return view_func(request, *args, **kwargs)

    return wrapper

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.users.middleware import firebase_auth_required
from apps.users import services
import random
import time
from django.core.mail import send_mail
from django.conf import settings

# In-memory OTP store: { email: { 'otp': str, 'expires': float } }
_otp_store = {}


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


@api_view(['GET'])
@firebase_auth_required
def list_all_users(request):
    """List all registered users (admin)."""
    users = services.get_all_users()
    return Response({'status': 'success', 'data': users})


# ─── Forgot Password OTP ───

@api_view(['POST'])
def send_otp(request):
    """Send a 6-digit OTP to the user's email via SMTP."""
    email = request.data.get('email', '').strip().lower()
    if not email:
        return Response(
            {'status': 'error', 'message': 'Email is required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Verify the email exists in Firebase Auth
    try:
        from firebase_admin import auth as fb_auth
        fb_auth.get_user_by_email(email)
    except Exception:
        return Response(
            {'status': 'error', 'message': 'No account found with this email.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    _otp_store[email] = {'otp': otp, 'expires': time.time() + 600}  # 10 min expiry

    # Send email
    try:
        send_mail(
            subject='TrustHut — Password Reset OTP',
            message=f'Your OTP for password reset is: {otp}\n\nThis code expires in 10 minutes.\nIf you did not request this, please ignore this email.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        return Response(
            {'status': 'error', 'message': f'Failed to send email: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response({'status': 'success', 'message': 'OTP sent to your email.'})


@api_view(['POST'])
def verify_otp_and_reset(request):
    """Verify OTP and reset the user's password in Firebase Auth."""
    email = request.data.get('email', '').strip().lower()
    otp = request.data.get('otp', '').strip()
    new_password = request.data.get('new_password', '')

    if not email or not otp or not new_password:
        return Response(
            {'status': 'error', 'message': 'Email, OTP, and new password are required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if len(new_password) < 8:
        return Response(
            {'status': 'error', 'message': 'Password must be at least 8 characters.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Verify OTP
    stored = _otp_store.get(email)
    if not stored:
        return Response(
            {'status': 'error', 'message': 'No OTP was requested for this email.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if time.time() > stored['expires']:
        del _otp_store[email]
        return Response(
            {'status': 'error', 'message': 'OTP has expired. Please request a new one.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if stored['otp'] != otp:
        return Response(
            {'status': 'error', 'message': 'Invalid OTP. Please try again.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # OTP valid — update password in Firebase Auth
    try:
        from firebase_admin import auth as fb_auth
        user = fb_auth.get_user_by_email(email)
        fb_auth.update_user(user.uid, password=new_password)
    except Exception as e:
        return Response(
            {'status': 'error', 'message': f'Failed to reset password: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Clean up OTP
    del _otp_store[email]

    return Response({'status': 'success', 'message': 'Password reset successful. You can now log in.'})


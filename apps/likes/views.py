from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.users.middleware import firebase_auth_required
from apps.likes import services
from apps.posts.services import get_post


@api_view(['POST'])
@firebase_auth_required
def like_post(request):
    """Like a post."""
    post_id = request.data.get('post_id')
    if not post_id:
        return Response(
            {'status': 'error', 'message': 'post_id is required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    post = get_post(post_id)
    if not post:
        return Response(
            {'status': 'error', 'message': 'Post not found.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    liked = services.like_post(request.firebase_uid, post_id)
    if not liked:
        return Response(
            {'status': 'error', 'message': 'Already liked this post.'},
            status=status.HTTP_409_CONFLICT,
        )

    return Response({'status': 'success', 'message': 'Post liked.'})


@api_view(['POST'])
@firebase_auth_required
def unlike_post(request):
    """Unlike a post."""
    post_id = request.data.get('post_id')
    if not post_id:
        return Response(
            {'status': 'error', 'message': 'post_id is required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    removed = services.unlike_post(request.firebase_uid, post_id)
    if not removed:
        return Response(
            {'status': 'error', 'message': 'You have not liked this post.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response({'status': 'success', 'message': 'Post unliked.'})


@api_view(['GET'])
@firebase_auth_required
def check_like(request, post_id):
    """Check if the current user has liked a post."""
    liked = services.has_user_liked(request.firebase_uid, post_id)
    return Response({'status': 'success', 'data': {'liked': liked}})

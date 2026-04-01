from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.users.middleware import firebase_auth_required
from apps.comments import services


@api_view(['POST'])
@firebase_auth_required
def add_comment(request):
    """Add a comment to a post (auth required)."""
    post_id = request.data.get('post_id', '')
    text = request.data.get('text', '').strip()

    if not post_id or not text:
        return Response(
            {'status': 'error', 'message': 'post_id and text are required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if len(text) > 1000:
        return Response(
            {'status': 'error', 'message': 'Comment must be under 1000 characters.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    comment = services.add_comment(request.firebase_uid, post_id, text)
    return Response(
        {'status': 'success', 'data': comment},
        status=status.HTTP_201_CREATED,
    )


@api_view(['GET'])
def get_comments(request, post_id):
    """Get all comments for a post (public)."""
    comments = services.get_comments(post_id)
    return Response({'status': 'success', 'data': comments})


@api_view(['DELETE'])
@firebase_auth_required
def delete_comment(request, comment_id):
    """Delete a comment (owner only)."""
    deleted = services.delete_comment(comment_id, request.firebase_uid)
    if not deleted:
        return Response(
            {'status': 'error', 'message': 'Comment not found or not authorized.'},
            status=status.HTTP_404_NOT_FOUND,
        )
    return Response({'status': 'success', 'message': 'Comment deleted.'})

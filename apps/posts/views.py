from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.users.middleware import firebase_auth_required
from apps.posts import services
from apps.posts.serializers import PostCreateSerializer, PostUpdateSerializer


@api_view(['POST'])
@firebase_auth_required
def create_post(request):
    """Create a new accessibility report post."""
    serializer = PostCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'status': 'error', 'message': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    post = services.create_post(request.firebase_uid, serializer.validated_data)
    return Response(
        {'status': 'success', 'message': 'Post created.', 'data': post},
        status=status.HTTP_201_CREATED,
    )


@api_view(['GET'])
def list_posts(request):
    """List all posts (public)."""
    posts = services.get_all_posts()
    return Response({'status': 'success', 'data': posts})


@api_view(['GET'])
def get_post(request, post_id):
    """Get a single post by ID (public)."""
    post = services.get_post(post_id)
    if not post:
        return Response(
            {'status': 'error', 'message': 'Post not found.'},
            status=status.HTTP_404_NOT_FOUND,
        )
    return Response({'status': 'success', 'data': post})


@api_view(['PUT'])
@firebase_auth_required
def update_post(request, post_id):
    """Update a post (owner or admin)."""
    post = services.get_post(post_id)
    if not post:
        return Response(
            {'status': 'error', 'message': 'Post not found.'},
            status=status.HTTP_404_NOT_FOUND,
        )


    serializer = PostUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'status': 'error', 'message': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    updated = services.update_post(post_id, serializer.validated_data)
    return Response({'status': 'success', 'data': updated})



# TO:
@api_view(['DELETE'])
@firebase_auth_required
def delete_post(request, post_id):
    post = services.get_post(post_id)
    if not post:
        return Response(
            {'status': 'error', 'message': 'Post not found.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    services.delete_post(post_id)
    return Response({'status': 'success', 'message': 'Post deleted.'})
    
@api_view(['GET'])
def search_posts(request):
    """Search posts by keyword (public)."""
    query = request.GET.get('q', '')
    if not query:
        return Response(
            {'status': 'error', 'message': 'Search query is required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    results = services.search_posts(query)
    return Response({'status': 'success', 'data': results})


@api_view(['GET'])
@firebase_auth_required
def user_posts(request):
    """Get posts by the authenticated user."""
    posts = services.get_user_posts(request.firebase_uid)
    return Response({'status': 'success', 'data': posts})


@api_view(['GET'])
def highway_risks(request):
    """Get all highway risk posts (public)."""
    risk_category = request.GET.get('risk_category', None)
    severity = request.GET.get('severity', None)
    posts = services.get_highway_risks(risk_category=risk_category, severity=severity)
    return Response({'status': 'success', 'data': posts})

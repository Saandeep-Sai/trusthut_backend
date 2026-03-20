from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.chatbot import services


@api_view(['POST'])
def chatbot_query(request):
    """Process a chatbot query (public — no auth required)."""
    query = request.data.get('query', '')

    if not query:
        return Response(
            {'status': 'error', 'message': 'Query is required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    result = services.process_query(query)
    return Response({
        'status': 'success',
        'data': result,
    })

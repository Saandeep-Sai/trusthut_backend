from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """Custom exception handler that returns consistent error format."""
    response = exception_handler(exc, context)

    if response is not None:
        return Response(
            {
                'status': 'error',
                'message': response.data.get('detail', str(response.data)),
            },
            status=response.status_code,
        )

    # Unhandled exceptions
    return Response(
        {
            'status': 'error',
            'message': 'An unexpected error occurred.',
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

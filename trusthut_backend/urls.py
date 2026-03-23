from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from datetime import datetime


def health_check(request):
    return JsonResponse({
        'status': 'ok',
        'service': 'trusthut-backend',
        'timestamp': datetime.utcnow().isoformat(),
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health-check'),
    path('api/users/', include('apps.users.urls')),
    path('api/posts/', include('apps.posts.urls')),
    path('api/', include('apps.likes.urls')),
    path('api/chatbot/', include('apps.chatbot.urls')),
]


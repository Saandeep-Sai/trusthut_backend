from django.urls import path
from apps.likes import views

urlpatterns = [
    path('like/', views.like_post, name='like-post'),
    path('unlike/', views.unlike_post, name='unlike-post'),
    path('like/check/<str:post_id>/', views.check_like, name='check-like'),
]

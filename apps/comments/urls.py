from django.urls import path
from apps.comments import views

urlpatterns = [
    path('', views.add_comment, name='add-comment'),
    path('<str:post_id>/', views.get_comments, name='get-comments'),
    path('delete/<str:comment_id>/', views.delete_comment, name='delete-comment'),
]

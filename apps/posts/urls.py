from django.urls import path
from apps.posts import views

urlpatterns = [
    path('create/', views.create_post, name='create-post'),
    path('', views.list_posts, name='list-posts'),
    path('search/', views.search_posts, name='search-posts'),
    path('user/', views.user_posts, name='user-posts'),
    path('<str:post_id>/', views.get_post, name='get-post'),
    path('update/<str:post_id>/', views.update_post, name='update-post'),
    path('delete/<str:post_id>/', views.delete_post, name='delete-post'),
]

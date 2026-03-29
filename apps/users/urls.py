from django.urls import path
from apps.users import views

urlpatterns = [
    path('register/', views.register_user, name='register-user'),
    path('profile/', views.profile, name='user-profile'),
    path('all/', views.list_all_users, name='list-all-users'),
]

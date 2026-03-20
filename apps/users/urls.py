from django.urls import path
from apps.users import views

urlpatterns = [
    path('register/', views.register_user, name='register-user'),
    path('profile/', views.profile, name='user-profile'),
]

from django.urls import path
from apps.users import views

urlpatterns = [
    path('register/', views.register_user, name='register-user'),
    path('profile/', views.profile, name='user-profile'),
    path('all/', views.list_all_users, name='list-all-users'),
    path('forgot-password/send-otp/', views.send_otp, name='send-otp'),
    path('forgot-password/verify-otp/', views.verify_otp_and_reset, name='verify-otp'),
]

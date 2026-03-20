from django.urls import path
from apps.chatbot import views

urlpatterns = [
    path('query/', views.chatbot_query, name='chatbot-query'),
]

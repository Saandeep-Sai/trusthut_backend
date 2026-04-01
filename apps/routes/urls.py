from django.urls import path
from apps.routes import views

urlpatterns = [
    path('score/', views.score_routes, name='score-routes'),
]

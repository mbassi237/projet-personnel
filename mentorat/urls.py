from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import path, include


from . import views
from .views import MentoringProgressView, MentoringViewSet, ListMentoringsView, MentoringAccepter

urlpatterns = [
    path('mentoring/', ListMentoringsView.as_view(), name='mentoring-list'),
    path('mentorship/progress/', MentoringProgressView.as_view(), name='mentoring-progress'),
    path('mentoring/requests/<int:pk>/respond/', MentoringAccepter.as_view({'patch': 'respond'}), name='mentoring-accept'),
    path('mentorship/demande/', MentoringViewSet.as_view({'post': 'create', 'get': 'list'}), name='mentoring-demande'),
    path('mentoring/chat/<int:mentoring_id>/messages/', views.MentoringMessageViewSet.as_view({'post': 'create', 'get': 'list'}), name='message'),
]
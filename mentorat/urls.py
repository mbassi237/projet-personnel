from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CreateMentorView,
    MentorListView,
    MentoringViewSet,
    MentoringAccepter,
    MentoringMessageViewSet,
    MentoringProgressView,
)

router = DefaultRouter()
#router.register(r'mentors', MentorViewSet, basename='mentors')
router.register(r'mentoring', MentoringViewSet, basename='mentoring')
#router.register(r'mentoringrespond/', MentoringAccepter, basename='mentoring-respond')
#router.register(r'mentoring/chat/', MentoringMessageViewSet, basename='mentoring-chat')

urlpatterns = [
    path('', include(router.urls)),
    path('mentors/list/', MentorListView.as_view(), name='mentor-list'),
    path('mentorship/progress/', MentoringProgressView.as_view(), name='mentoring-progress'),
    path('mentoring/requests/<int:pk>/respond/', MentoringAccepter.as_view({'patch': 'respond'}), name='mentoring-accept'),
    path('mentors/', CreateMentorView.as_view(), name='mentor'),
path('mentoring/chat/<int:mentoring_id>/messages/', MentoringMessageViewSet.as_view({'post': 'create', 'get': 'list'}), name='message'),
    #path('mentorship/all/', ListMentoringsView.as_view(), name='list-mentorships'),
]
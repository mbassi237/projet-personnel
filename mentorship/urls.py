
from django.urls import path
from .views import (
    MentoringIntroductionView,
    MentorSearchView,
    MentorRecommendationView,
    RequestMentorView,
    MentoringProgressView
)

urlpatterns = [
    # Acces a la page d'introduction au mentorat
    path('mentorship/', MentoringIntroductionView.as_view(), name='mentoring-introduction'),
    path('mentorship/search/', MentorSearchView.as_view(), name='mentor-search'),
    path('mentorship/recommend/', MentorRecommendationView.as_view(), name='mentor-recommendation'),
    path('mentorship/progress/', MentoringProgressView.as_view(), name='mentoring-progress'),
]
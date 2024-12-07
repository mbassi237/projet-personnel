
from django.urls import path
from .views import (
    EventListView,
    EventDetailView,
    AddToCalendarView
)

urlpatterns = [
    # Endpoint pour lister les ressources avec recherche et filtres
    path('evenements/', EventListView.as_view(), name='event-list'),
    path('evenements/<int:event_id>/', EventDetailView.as_view(), name='event-detail'),
    path('evenements/<int:event_id>/calendar/', AddToCalendarView.as_view(), name='event-add-to-calendar')
]

from django.urls import path

from formation.views import RessourceListView, CreateRessourceView

urlpatterns = [
    # Endpoint pour lister les ressources avec recherche et filtres
    path('formation/', RessourceListView.as_view(), name='ressource-list'),
    path('formation/create/', CreateRessourceView.as_view(), name='create-ressource')
]
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
#from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from formation.models import Ressources
from formation.serializers import RessourceSerializer


# Create your views here.

class CreateRessourceView(APIView):
    """
    Vue pour creer une ressource de formation
    """

    #permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RessourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.CustomUser)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RessourceListView(APIView):
    def get(self, request):
        """Rechercher et filtrer des ressources"""
        query = request.query_params.get('q', '') # Rechercher par mot-cles
        ressource_type = request.query_params.get('type', '') # filtrer par type
        difficulty = request.query_params.get('difficulty', '') # filtre par difficulte
        tags = request.query_params.getlist('tags', []) # Filtrer par tags

        ressources = Ressources.objects.all()

        # Appliquer les filtres
        if query:
            ressources = ressources.filter(Q(Title__icontains=query) | Q(Description__icontains=query))
        if ressource_type:
            ressources = ressources.filter(ressource_type=ressource_type)
        if difficulty:
            ressources = ressources.filter(difficulty_level=difficulty)
        if tags:
            ressources = ressources.filter(tags__overlap=tags)

        serializer = RessourceSerializer(ressources, many=True)
        return Response(serializer.data)
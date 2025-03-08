from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from formation.models import Ressources
from formation.serializers import RessourceSerializer
from formation.authentication import MicroserviceTokenAuthentication

# Create your views here.

class CreateRessourceView(APIView):
    """
    Vue pour creer une ressource de formation
    """
    authentication_classes = [MicroserviceTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        serializer = RessourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=user_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RessourceListView(APIView):
    """
    Vue pour rechercher et filtrer les ressources éducatives.
    """
    authentication_classes = [MicroserviceTokenAuthentication]  #Appliquer l'authentification externe
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Rechercher et filtrer des ressources.
        """
        # Vérifier que l'utilisateur est bien authentifié via le microservice
        if not request.user:
            return Response({"error": "Utilisateur non authentifié"}, status=401)

        # Récupérer les paramètres de recherche
        query = request.query_params.get('q', '')  #Rechercher par mots-clés
        ressource_type = request.query_params.get('type', '')  #Filtrer par type
        difficulty = request.query_params.get('difficulty', '')  #Filtrer par difficulté
        tags = request.query_params.getlist('tags', [])  #Filtrer par tags

        # Récupérer toutes les ressources
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

        # Sérialiser les ressources
        serializer = RessourceSerializer(ressources, many=True)
        return Response(serializer.data, status=200)
from django.db.models import Q
from django.shortcuts import render
import requests
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
    Vue pour créer une ressource de formation.
    """
    authentication_classes = [MicroserviceTokenAuthentication]  # Utilisation de l'authentification externe
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Permet à un utilisateur authentifié de créer une ressource.
        """
        # Vérifier que l'utilisateur est bien authentifié via le microservice
        if not request.user:
            return Response({"error": "Utilisateur non authentifié"}, status=status.HTTP_401_UNAUTHORIZED)

        # Récupérer l'ID de l'utilisateur et ses infos depuis le microservice
        user_id = request.user.id
        user_info = {
            "id": user_id,
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }

        # Ajouter l’auteur à la requête avant validation
        data = request.data.copy()
        data["Author_Id"] = user_id  # Stocker seulement l'ID de l'auteur dans la BD

        # Sérialisation et validation
        serializer = RessourceSerializer(data=data)
        if serializer.is_valid():
            ressource = serializer.save()  # L’auteur est enregistré avec la ressource

            # Construction de la réponse avec les infos utilisateur
            response_data = serializer.data
            response_data["author_info"] = user_info  # Ajout des infos utilisateur

            return Response(response_data, status=status.HTTP_201_CREATED)

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
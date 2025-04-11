from django.shortcuts import render

# Create your views here.

from django.db import models
from django.contrib.auth.models import User
from rest_framework import status, viewsets, filters, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from datetime import datetime

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Mentoring, MentoringMessage
from .serializers import MentoringSerializer, MentoringMessageSerializer
from mentorat.authentication import MicroserviceTokenAuthentication
import requests


class MentoringViewSet(viewsets.ViewSet):
    authentication_classes = [MicroserviceTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # Créer une demande de mentorat (Mentee)
    def create(self, request):
        serializer = MentoringSerializer(data=request.data)
        if serializer.is_valid():
            # Récupérer l'ID du mentor depuis la requête
            mentor_id = serializer.validated_data["mentor_id"]

            # Récupérer l'ID du mentee depuis le service d'authentification
            mentee_id = request.user.id  # Supposons que le service renvoie un ID numérique

            mentoring = Mentoring.objects.create(
                mentor_id=mentor_id,
                mentee_id=mentee_id,
                Start_Date=serializer.validated_data.get("Start_Date"),
                End_Date=serializer.validated_data.get("End_Date"),
                Status="active"
            )
            return Response(MentoringSerializer(mentoring).data, status=201)
        return Response(serializer.errors, status=400)

    # Liste des demandes de mentorat (Mentor/Mentee)
    def list(self, request):
        user_id = request.user.id  # ID de l'utilisateur authentifié
        mentorings = Mentoring.objects.filter(mentor_id=user_id) | Mentoring.objects.filter(mentee_id=user_id)
        serializer = MentoringSerializer(mentorings, many=True)
        return Response(serializer.data)



class MentoringAccepter(viewsets.ViewSet):
    authentication_classes = [MicroserviceTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # Accepter/Rejeter une demande (Mentor) Permet au mentor d’accepter (active) ou rejeter (inactive) une demande.
    @action(detail=True, methods=['patch'])
    def respond(self, request, pk=None):
        mentoring = Mentoring.objects.get(id=pk)
        if mentoring.mentor_id != request.user.id:
            return Response({"error": "Permission denied"}, status=403)

        new_status = request.data.get('status')
        if new_status in ['active', 'inactive']:
            mentoring.Status = new_status
            mentoring.save()
            return Response(MentoringSerializer(mentoring).data)
        return Response({"error": "Statut invalide"}, status=400)

class MentoringMessageViewSet(viewsets.ViewSet):
    authentication_classes = [MicroserviceTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # Envoyer un message dans le chat
    # Envoyer un message dans le chat
    def create(self, request, mentoring_id=None):
        mentoring = Mentoring.objects.get(id=mentoring_id)
        sender_id = str(request.user.id)  # Convertir en chaîne pour correspondre au modèle

        # Vérifier que l'utilisateur est mentor ou mentee
        if request.user.id not in [mentoring.mentor_id, mentoring.mentee_id]:
            return Response({"error": "Accès non autorisé"}, status=403)

        message = MentoringMessage.objects.create(
            mentoring=mentoring,
            sender_id=sender_id,
            message=request.data['message']
        )
        return Response({"id": message.id, "message": message.message}, status=201)

    # Lister les messages d'un mentorat
    def list(self, request, mentoring_id=None):
        messages = MentoringMessage.objects.filter(mentoring_id=mentoring_id)
        serializer = MentoringMessageSerializer(messages, many=True)
        return Response(serializer.data)




class MentoringProgressView(APIView):
    """
    Suivi des progrès de l'utilisateur dans le cadre du mentorat.
    """
    authentication_classes = [MicroserviceTokenAuthentication]  # Appliquer l'authentification
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Récupère la progression du mentorat pour l'utilisateur connecté via le microservice.
        """
        # Vérifier que l'utilisateur est bien authentifié via le microservice
        if not request.user:
            return Response({"error": "Utilisateur non authentifié"}, status=status.HTTP_401_UNAUTHORIZED)

        # Récupérer les informations de l'utilisateur
        mentee_id = request.user.id
        mentee_info = {
            "id": mentee_id,
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }

        # Filtrer les mentorats actifs de l'utilisateur (en tant que mentee)
        mentorings = Mentoring.objects.filter(Status="active").order_by('-Start_Date')

        if not mentorings.exists():
            return Response({"message": "Aucune relation de mentorat active trouvée"}, status=status.HTTP_404_NOT_FOUND)

        data = []
        for mentoring in mentorings:
            # Simulation d'une récupération de mentor via le service d'authentification
            mentor_info = {
                "id": mentoring.id,  # À remplacer par une récupération via l'API d'authentification
                "username": f"Mentor_{mentoring.id}",
                "phone_number": "Non disponible",
                "is_verified": True  # Valeur fictive à remplacer par la vraie donnée
            }

            data.append({
                "mentee_info": mentee_info,
                "mentor_info": mentor_info,
                "Start_Date": mentoring.Start_Date,
                "End_Date": mentoring.End_Date,
                "Status": mentoring.Status,
                "Created_At": mentoring.Created_At,
                "Updated_At": mentoring.Updated_At
            })

        return Response(data, status=status.HTTP_200_OK)




class ListMentoringsView(APIView):
    """
    Vue pour lister tous les mentorats existants de l'utilisateur connecté,
    qu'il soit mentor ou mentee.
    """
    authentication_classes = [MicroserviceTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id

        # Récupérer les mentorats où l'utilisateur est mentee ou mentor
        mentorings = Mentoring.objects.filter(
            mentor_id=user_id
        ) | Mentoring.objects.filter(
            mentee_id=user_id
        )

        serializer = MentoringSerializer(mentorings.distinct(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
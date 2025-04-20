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
from .models import Mentoring, MentoringMessage, Mentor
from .serializers import MentoringSerializer, MentoringMessageSerializer, MentorSerializer
from mentorat.authentication import MicroserviceTokenAuthentication
import requests


# ----------------------- Vue pour Créer un mentor -------------------------
class CreateMentorView(APIView):
    """
    Vue pour créer un profil de mentor.
    """
    authentication_classes = [MicroserviceTokenAuthentication]  # Authentification via service externe
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Permet à un utilisateur authentifié de s'enregistrer comme mentor.
        """
        # Vérifier l'authentification
        if not request.user:
            return Response({"error": "Utilisateur non authentifié"}, status=status.HTTP_401_UNAUTHORIZED)

        # Infos utilisateur récupérées depuis le service d'authentification
        user_info = {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name
        }

        data = request.data.copy()

        # Sérialisation et validation
        serializer = MentorSerializer(data=data)
        if serializer.is_valid():
            mentor = serializer.save()

            response_data = serializer.data
            response_data["user_info"] = user_info  # Ajout des infos de l'utilisateur connecté

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------- Créer et Lister les mentorats -------------------------
class MentoringViewSet(viewsets.ViewSet):
    authentication_classes = [MicroserviceTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        """
        Créer une demande de mentorat à partir du nom du mentor.
        Le mentoré est automatiquement défini comme l'utilisateur connecté.
        """
        # Authentification de l'utilisateur connecté (mentee)
        mentee_id = request.user.id

        # Récupération des champs envoyés
        mentor_name = request.data.get("Nom_mentor")
        start_date = request.data.get("Start_Date")
        end_date = request.data.get("End_Date")

        # Vérification du mentor dans la base
        try:
            mentor = Mentor.objects.get(Nom_mentor__iexact=mentor_name)
        except Mentor.DoesNotExist:
            return Response({"error": f"Aucun mentor avec le nom '{mentor_name}'"}, status=404)

        # Création de l'objet Mentoring
        mentoring = Mentoring.objects.create(
            Mentor_Id=mentor,
            mentee_id=mentee_id,
            Start_Date=start_date,
            End_Date=end_date,
            Status="active"
        )

        # Réponse structurée
        response = {
            "mentee_id": mentee_id,
            "mentor": {
                "id": mentor.id,
                "nom": mentor.Nom_mentor,
                "prenom": mentor.Prenom_mentor,
                "profession": mentor.Profession
            },
            "Start_Date": mentoring.Start_Date,
            "End_Date": mentoring.End_Date,
            "Status": mentoring.Status,
            "Created_At": mentoring.Created_At,
            "Updated_At": mentoring.Updated_At
        }

        return Response(response, status=201)

    def list(self, request):
        user_id = request.user.id
        mentorings = Mentoring.objects.filter(mentee_id=user_id) | Mentoring.objects.filter(Mentor_Id__id=user_id)
        serializer = MentoringSerializer(mentorings.distinct(), many=True)
        return Response(serializer.data)


# ----------------------- Accepter une demande -------------------------
class MentoringAccepter(viewsets.ViewSet):
    authentication_classes = [MicroserviceTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['patch'])
    def respond(self, request, pk=None):
        mentoring = get_object_or_404(Mentoring, id=pk)
        if mentoring.Mentor_Id.id != request.user.id:
            return Response({"error": "Permission denied"}, status=403)
        new_status = request.data.get('status')
        if new_status in ['active', 'inactive']:
            mentoring.Status = new_status
            mentoring.save()
            return Response(MentoringSerializer(mentoring).data)
        return Response({"error": "Statut invalide"}, status=400)


# ----------------------- Chat entre mentoré et mentor -------------------------
class MentoringMessageViewSet(viewsets.ViewSet):
    authentication_classes = [MicroserviceTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, mentoring_id=None):
        mentoring = get_object_or_404(Mentoring, id=mentoring_id)
        sender_id = str(request.user.id)
        if request.user.id not in [mentoring.mentee_id, mentoring.Mentor_Id.id]:
            return Response({"error": "Accès non autorisé"}, status=403)

        message = MentoringMessage.objects.create(
            mentoring=mentoring,
            sender_id=sender_id,
            message=request.data['message']
        )
        return Response({"id": message.id, "message": message.message}, status=201)

    def list(self, request, mentoring_id=None):
        messages = MentoringMessage.objects.filter(mentoring_id=mentoring_id)
        serializer = MentoringMessageSerializer(messages, many=True)
        return Response(serializer.data)


# ----------------------- Progression de mentorat -------------------------
class MentoringProgressView(APIView):
    authentication_classes = [MicroserviceTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        mentee_id = request.user.id
        mentorings = Mentoring.objects.filter(mentee_id=mentee_id, Status="active")

        if not mentorings.exists():
            return Response({"message": "Aucune relation de mentorat active trouvée"}, status=404)

        data = []
        for mentoring in mentorings:
            mentor = mentoring.Mentor_Id
            data.append({
                "mentee_info": {
                    "id": mentee_id,
                    "username": request.user.username
                },
                "mentor_info": {
                    "id": mentor.id,
                    "nom": mentor.Nom_mentor,
                    "prenom": mentor.Prenom_mentor,
                    "profession": mentor.Profession
                },
                "Start_Date": mentoring.Start_Date,
                "End_Date": mentoring.End_Date,
                "Status": mentoring.Status,
                "Created_At": mentoring.Created_At,
                "Updated_At": mentoring.Updated_At
            })

        return Response(data, status=200)


# ----------------------- Liste des mentors -------------------------
class MentorListView(APIView):
    authentication_classes = [MicroserviceTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        mentors = Mentor.objects.all()
        serializer = MentorSerializer(mentors, many=True)
        return Response(serializer.data)
from django.shortcuts import render

# Create your views here.
import urllib.parse
from formation.authentication import MicroserviceTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Events
from rest_framework import status
from .serializers import EventSerializer




class CreateEventView(APIView):
    """
    Vue pour créer un événement.
    """
    authentication_classes = [MicroserviceTokenAuthentication]  # Utilisation de l'authentification externe
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Permet à un utilisateur authentifié de créer un événement.
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

        # Ajouter l’organisateur à la requête avant validation
        data = request.data.copy()
        data["Organized_By"] = user_id  # Stocke seulement l'ID de l’organisateur dans la BD

        # Sérialisation et validation
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            event = serializer.save()  # L’organisateur est enregistré avec l’événement

            # Construction de la réponse avec les infos utilisateur
            response_data = serializer.data
            response_data["organizer_info"] = user_info  # Ajout des infos utilisateur

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventListView(APIView):
    """
    Vue pour rechercher et filtrer les événements.
    """
    authentication_classes = [MicroserviceTokenAuthentication]  #Appliquer l'authentification externe
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Récupérer une liste d'événements avec recherche et filtres.
        """
        # Vérifier que l'utilisateur est bien authentifié via le microservice
        if not request.user:
            return Response({"error": "Utilisateur non authentifié"}, status=401)

        # Récupérer les paramètres de recherche et de filtrage
        query = request.query_params.get('q', '')  #Recherche par mots-clés
        category = request.query_params.get('category', '')  #Filtrer par catégorie
        theme = request.query_params.get('theme', '')  #Filtrer par thème
        event_format = request.query_params.get('format', '')  # Filtrer par format
        is_free = request.query_params.get('is_free', None)  #Filtrer si l'événement est gratuit ou payant

        # Récupérer tous les événements
        events = Events.objects.all()

        # Appliquer les filtres
        if query:
            events = events.filter(Q(Title__icontains=query) | Q(Description__icontains=query))
        if category:
            events = events.filter(category=category)
        if theme:
            events = events.filter(theme=theme)
        if event_format:
            events = events.filter(format=event_format)
        if is_free is not None:
            events = events.filter(is_free=(is_free.lower() == 'true'))

        # Sérialiser les événements
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=200)




class EventDetailView(APIView):
    """
    Vue pour afficher les détails d'un événement spécifique.
    """
    authentication_classes = [MicroserviceTokenAuthentication]  #Utiliser l'authentification externe
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        """
        Récupérer les détails d'un événement spécifique.
        """
        # Vérifier que l'utilisateur est bien authentifié via le microservice
        if not request.user:
            return Response({"error": "Utilisateur non authentifié"}, status=401)

        # Vérifier si l'événement existe
        try:
            event = Events.objects.get(id=event_id)
        except Events.DoesNotExist:
            return Response({'error': 'Événement non trouvé'}, status=404)

        # Sérialiser et retourner les détails de l'événement
        serializer = EventSerializer(event)
        return Response(serializer.data, status=200)



class AddToCalendarView(APIView):
    """
    Vue pour ajouter un événement au calendrier personnel de l'utilisateur.
    """
    authentication_classes = [MicroserviceTokenAuthentication]  #Utiliser l'authentification externe
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        """
        Générer un lien Google Calendar pour la synchronisation.
        """
        # Vérifier que l'utilisateur est bien authentifié via le microservice
        if not request.user:
            return Response({"error": "Utilisateur non authentifié"}, status=401)

        # Vérifier si l'événement existe
        try:
            event = Events.objects.get(id=event_id)
        except Events.DoesNotExist:
            return Response({'error': 'Événement non trouvé'}, status=404)

        # Encodage des détails pour éviter les erreurs dans l'URL
        event_title = urllib.parse.quote(event.Title)
        event_description = urllib.parse.quote(event.Description)
        event_location = urllib.parse.quote(event.Localisation)

        # Format de date ISO 8601 pour Google Calendar (YYYYMMDDTHHMMSSZ)
        start_date = event.Start_Date_Time.strftime('%Y%m%dT%H%M%SZ')
        end_date = event.End_Date_Time.strftime('%Y%m%dT%H%M%SZ')

        # Génération du lien Google Calendar
        calendar_link = (
            f"https://www.google.com/calendar/render?action=TEMPLATE"
            f"&text={event_title}"
            f"&dates={start_date}/{end_date}"
            f"&details={event_description}"
            f"&location={event_location}"
            f"&sf=true&output=xml"
        )

        return Response({'calendar_link': calendar_link}, status=200)
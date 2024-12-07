from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Events
from .serializers import EventSerializer


class EventListView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        category = request.query_params.get('category', '')
        theme = request.query_params.get('theme')
        format = request.query_params.get('format')
        is_free = request.query_params.get('is_free', None)

        events = Events.objects.all()

        # Appliquer les filtres
        if query:
            events = events.filter(Q(Title__icontains=query) | Q(Description__icontains=query))
        if category:
            events = events.filter(category=category)
        if theme:
            events = events.filter(theme=theme)
        if format:
            events = events.filter(format=format)
        if is_free is not None:
            events = events.filter(is_free=(is_free.lower() == 'true'))

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)




class EventDetailView(APIView):
    """
    Vue pour afficher les details d'un evenement et permettre l'inscription
    """
    def get(self, request, event_id):
        """
        Recuperer les details d'un evenement specifique.
        """
        try:
            event = Events.objects.get(id=event_id)
        except Events.DoesNotExist:
            return Response({'error': 'Evenement non trouve'}, status=404)
        serializer = EventSerializer(event)
        return Response(serializer.data)



class AddToCalendarView(APIView):
    """
    Vue pour ajouter un evenement au calendrier personnel de l'utilisateur.
    """
    def post(self, request, event_id):
        """
        Generer un lien de calendrier pour une synchronisation
        :param request:
        :param event_id:
        :return:
        """
        try:
            event = Events.objects.get(id=event_id)
        except Events.DoesNotExist:
            return  Response({'error': 'Evenement non trouve'}, status=404)

        # Exemple simple de lien pour Google calendar
        calendar_link = f"https://www.google.com/calendar/render?action=TEMPLATE&text={event.title}&dates={event.start_date_time.isoformat()}/{event.end_date_time.isoformat()}&details={event.Description}&location={event.Localisation}"
        return Response({'calendar_link': calendar_link})
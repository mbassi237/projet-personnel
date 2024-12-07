from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response

from mentorship.models import Mentoring
from mentorship.serializers import MentoringSerializer
from user.models import CustomUser


class MentoringIntroductionView(APIView):
    """
    Vue d'introduction au mentorat
    """
    def get(self, request):
        """
        Affiche des informations sur le mentorat
        :param request:
        :return:
        """
        data = {
            'title': 'Bienvenue au système de mentorat',
            'description': 'Le mentorat vous aide à trouver des mentors qui vous guideront dans votre parcours personnel et professionnel.',
            'steps': [
                'Remplissez le formulaire pour préciser vos besoins',
                'Consultez les mentors disponibles',
                'Envoyez une demande de connexion au mentor de votre choix',
                'Commencez vos sessions de mentorat avec des interactions sécurisées'
            ]
        }
        return Response(data)




class MentorSearchView(APIView):
    """
    Recherche de mentors selon les besoins de l'utilisateur.
    """
    def get(self, request):
        """
        Recherche des mentors selon les critères fournis.
        """
        skills = request.query_params.get('skills', '')
        location = request.query_params.get('location', '')
        language = request.query_params.get('language', '')

        mentors = CustomUser.objects.filter(role='mentor')

        if skills:
            mentors = mentors.filter(skills__icontains=skills)
        if location:
            mentors = mentors.filter(location__icontains=location)
        if language:
            mentors = mentors.filter(language__icontains=language)

        serializer = MentoringSerializer(mentors, many=True)
        return Response(serializer.data)




class MentorRecommendationView(APIView):
    """
    Recommande des mentors a l'utilisateurs.
    """
    def get(self, request):
        """
        Recupere une liste de mentors correspondant aux besoins de l'utilisateur.
        :param request:
        :return:
        """
        # Pour l'instant, retourne les 5 premiers mentors les plus qualifies
        mentors = CustomUser.objects.filter(role='mentor')[:5]
        serializer = MentoringSerializer(mentors, many=True)
        return Response(serializer.data)




class RequestMentorView(APIView):
    """
    Vue pour permettre a un utilisateur de demander un mentor.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, mentor_id):
        """
        Permet a un utilisateur de demander un mentor
        :param request:
        :param mentor_id:
        :return:
        """
        data = {
            'Mentor_Id': mentor_id,
            'Mentee_Id': request.user.id,
            'Start_Date': request.data.get('Start_Date'),
            'End_Date': request.data.get('End_Date')
        }

        serializer = MentoringSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



class MentoringProgressView(APIView):
    """
    Suivi des progres de l'utilisateur dans le cadre du mentorat.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Affiche la progression de l'utilisateur dans le mentorat.
        :param request:
        :return:
        """
        mentorings = Mentoring.objects,filter(Mentee_Id=request.user)
        data = []

        for mentoring in mentorings:
            data.append({
                'Mentor': mentoring.Mentor_Id.username,
                'Start_Date': mentoring.Start_Date,
                'End_Date': mentoring.End_Date,
                'Status': mentoring.Status
            })
        return Response(data)
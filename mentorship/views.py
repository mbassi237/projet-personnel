from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from mentorship.authentication import MicroserviceTokenAuthentication
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
    Recherche de mentors selon les besoins de l'utilisateur en interrogeant le microservice d'authentification.
    """
    authentication_classes = [MicroserviceTokenAuthentication]  #Utiliser l'authentification externe
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Recherche des mentors selon les critères fournis.
        """
        # Vérifier que l'utilisateur est bien authentifié via le microservice
        if not request.user:
            return Response({"error": "Utilisateur non authentifié"}, status=401)

        # Récupération des critères de recherche
        skills = request.query_params.get('skills', '')  #Filtre par compétences
        location = request.query_params.get('location', '')  #Filtre par localisation
        language = request.query_params.get('language', '')  #Filtre par langue

        #URL du microservice d'auth pour récupérer les mentors
        mentors_api_url = "https://rajapi-cop-auth-api.onrender.com/auth/mentors/"

        try:
            # Envoyer une requête GET avec les filtres comme paramètres
            params = {
                "skills": skills,
                "location": location,
                "language": language
            }
            response = request.get(mentors_api_url, params=params)

            if response.status_code != 200:
                return Response({"error": "Impossible de récupérer les mentors"}, status=500)

            mentors_data = response.json()

            # Sérialiser les mentors récupérés depuis le microservice
            serializer = MentoringSerializer(mentors_data, many=True)
            return Response(serializer.data, status=200)

        except request.RequestException:
            return Response({"error": "Service d'authentification indisponible"}, status=503)




class MentorRecommendationView(APIView):
    """
    Recommande des mentors à l'utilisateur en interrogeant le microservice d'authentification.
    """
    authentication_classes = [MicroserviceTokenAuthentication]  #Utiliser l'authentification externe
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Récupère une liste de mentors recommandés depuis le microservice.
        """
        # Vérifier que l'utilisateur est bien authentifié via le microservice
        if not request.user:
            return Response({"error": "Utilisateur non authentifié"}, status=401)

        # 🔹 URL de l'API d'auth externe pour récupérer les mentors
        mentors_api_url = "https://rajapi-cop-auth-api.onrender.com/auth/mentors/"

        try:
            # Envoyer une requête GET pour récupérer la liste des mentors
            response = request.get(mentors_api_url)
            if response.status_code != 200:
                return Response({"error": "Impossible de récupérer la liste des mentors"}, status=500)

            mentors_data = response.json()

            # Filtrer pour prendre uniquement les 5 premiers mentors recommandés
            top_mentors = mentors_data[:5]

            # Sérialiser les mentors récupérés depuis le microservice
            serializer = MentoringSerializer(top_mentors, many=True)
            return Response(serializer.data, status=200)

        except request.RequestException:
            return Response({"error": "Service d'authentification indisponible"}, status=503)




class RequestMentorView(APIView):
    """
    Vue pour permettre à un utilisateur de demander un mentor.
    """
    authentication_classes = [MicroserviceTokenAuthentication]  #Utiliser l'authentification externe
    permission_classes = [IsAuthenticated]

    def post(self, request, mentor_id):
        """
        Permet à un utilisateur de demander un mentor.
        """
        # Vérifier que l'utilisateur est bien authentifié via le microservice
        if not request.user:
            return Response({"error": "Utilisateur non authentifié"}, status=401)

        user_id = request.user["id"]  #Récupérer l'ID du mentee depuis l'authentification externe
        mentor_id = int(mentor_id)  #S'assurer que l'ID du mentor est un entier

        # Vérifier si l'utilisateur n'essaie pas de se mentorer lui-même
        if user_id == mentor_id:
            return Response({"error": "Vous ne pouvez pas être votre propre mentor"}, status=400)

        # Vérifier si une relation de mentorat existe déjà
        existing_mentorship = Mentoring.objects.filter(Mentor_Id=mentor_id, Mentee_Id=user_id, Status="active").exists()

        if existing_mentorship:
            return Response({"error": "Vous avez déjà un mentorat actif avec cet utilisateur"}, status=400)

        # Récupérer les données de la requête
        start_date = request.data.get('Start_Date')
        end_date = request.data.get('End_Date')

        # Vérifier les dates
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

            if end_date_obj <= start_date_obj:
                return Response({"error": "La date de fin doit être après la date de début"}, status=400)
        except ValueError:
            return Response({"error": "Format de date invalide, utilisez YYYY-MM-DD"}, status=400)

        # Créer la demande de mentorat
        mentorship = Mentoring.objects.create(
            Mentor_Id=mentor_id,
            Mentee_Id=user_id,
            Start_Date=start_date,
            End_Date=end_date
        )

        # Sérialiser la réponse avec le `MentoringSerializer`
        serializer = MentoringSerializer(mentorship)

        return Response({
            "message": "Demande de mentorat créée avec succès",
            "mentoring": serializer.data
        }, status=201)


class MentoringProgressView(APIView):
    """
    Suivi des progrès de l'utilisateur dans le cadre du mentorat.
    """
    authentication_classes = [MicroserviceTokenAuthentication]  #Appliquer l'authentification
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Récupère la progression du mentorat pour l'utilisateur connecté via le microservice.
        """
        # Vérifier que l'utilisateur est bien authentifié via le microservice
        if not request.user:
            return Response({"error": "Utilisateur non authentifié"}, status=401)

        # Récupérer l'ID et l'email de l'utilisateur à partir du token validé
        user_email = request.user.email
        user_id = request.user.id

        # Filtrer les mentorats où l'utilisateur est mentee
        mentorings = Mentoring.objects.filter(Mentee_Id=user_id, Status="active").order_by('-Start_Date')

        if not mentorings.exists():
            return Response({"message": "Aucune relation de mentorat active trouvée"}, status=404)

        data = []
        for mentoring in mentorings:
            mentor = mentoring.Mentor_Id  # Récupération du mentor

            data.append({
                'Mentor': {
                    'username': mentor.username,
                    'phone_number': mentor.phone_number,
                    'is_verified': mentor.is_verified
                },
                'Start_Date': mentoring.Start_Date,
                'End_Date': mentoring.End_Date,
                'Status': mentoring.Status,
                'Created_At': mentoring.Created_At,
                'Updated_At': mentoring.Updated_At
            })

        return Response(data, status=200)
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from formation.authentication import MicroserviceTokenAuthentication
from mentorship.models import Mentoring
from rest_framework import status
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
    authentication_classes = [MicroserviceTokenAuthentication]  # Utiliser l'authentification externe
    permission_classes = [IsAuthenticated]

    def post(self, request, mentor_id):
        """
        Permet à un utilisateur de demander un mentor.
        """
        # Vérifier que l'utilisateur est bien authentifié via le microservice
        if not request.user:
            return Response({"error": "Utilisateur non authentifié"}, status=status.HTTP_401_UNAUTHORIZED)

        # Récupérer les infos du mentee depuis le microservice
        mentee_id = request.user.id
        mentee_info = {
            "id": mentee_id,
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }

        # Convertir `mentor_id` en entier
        try:
            mentor_id = int(mentor_id)
        except ValueError:
            return Response({"error": "ID du mentor invalide"}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier si l'utilisateur essaie de se mentorer lui-même
        if mentee_id == mentor_id:
            return Response({"error": "Vous ne pouvez pas être votre propre mentor"}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier si une relation de mentorat existe déjà
        existing_mentorship = Mentoring.objects.filter(
            Start_Date__lte=datetime.now().date(),
            End_Date__gte=datetime.now().date(),
            Status="active"
        ).exists()

        if existing_mentorship:
            return Response({"error": "Vous avez déjà un mentorat actif avec cet utilisateur"}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier les dates envoyées
        start_date = request.data.get("Start_Date")
        end_date = request.data.get("End_Date")

        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

            if end_date_obj <= start_date_obj:
                return Response({"error": "La date de fin doit être après la date de début"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Format de date invalide, utilisez YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        # Créer la relation de mentorat
        mentorship = Mentoring.objects.create(
            Start_Date=start_date_obj,
            End_Date=end_date_obj
        )

        # Sérialisation de la relation
        serializer = MentoringSerializer(mentorship)

        # Ajouter les infos du mentor et mentee dans la réponse API
        response_data = serializer.data
        response_data["mentee_info"] = mentee_info
        response_data["mentor_id"] = mentor_id  # Affichage de l'ID du mentor

        return Response({
            "message": "Demande de mentorat créée avec succès",
            "mentoring": response_data
        }, status=status.HTTP_201_CREATED)


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
import logging
import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.conf import settings

# Configuration du logger
logger = logging.getLogger(__name__)

class MicroserviceTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Récupérer le token depuis l'en-tête Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            logger.warning("Aucun en-tête Authorization trouvé dans la requête.")
            return None

        try:
            # Extraire le token en supprimant 'Bearer '
            token = auth_header.split(' ')[1]
        except IndexError:
            logger.error("Format du token invalide. L'en-tête Authorization doit être sous la forme 'Bearer <token>'.")
            return None

        # Vérifier si l'URL de vérification est bien configurée
        verify_url = 'https://rajapi-cop-auth-api.onrender.com/auth/token/verify'
        if not verify_url:
            logger.critical("L'URL de vérification du token (settings.URL_V) n'est pas configurée.")
            raise AuthenticationFailed({
                "code": "CONFIGURATION_ERROR",
                "detail": "Erreur de configuration interne. Contactez l'administrateur."
            })

        try:
            # Envoyer une requête de vérification
            response = requests.post(verify_url, json={'token': token}, timeout=5)
            response_data = response.json()
        except requests.Timeout:
            logger.error("Délai d'attente dépassé lors de la communication avec le microservice d'authentification.")
            raise AuthenticationFailed({
                "code": "AUTH_SERVICE_TIMEOUT",
                "detail": "Le service d'authentification est temporairement indisponible."
            })
        except requests.RequestException as e:
            logger.error(f"Erreur de communication avec le microservice d'authentification: {e}")
            raise AuthenticationFailed({
                "code": "TOKEN_VERIFICATION_FAILED",
                "detail": "Impossible de vérifier le token."
            })
        except ValueError:
            logger.error("Réponse JSON invalide reçue depuis le microservice d'authentification.")
            raise AuthenticationFailed({
                "code": "INVALID_AUTH_SERVICE_RESPONSE",
                "detail": "Réponse invalide du service d'authentification."
            })

        # Vérifier la validité du token
        if response.status_code != 200 or not response_data.get("token_valid", False):
            logger.warning("Token invalide ou expiré.")
            raise AuthenticationFailed({
                "code": "INVALID_OR_EXPIRED_TOKEN",
                "detail": "Token invalide ou expiré."
            })

        # Récupérer les informations utilisateur
        user_data = response_data.get('user_profile', {})
        if not user_data or not all(k in user_data for k in ['email', 'username']):
            logger.error(f"Données utilisateur manquantes ou incomplètes: {user_data}")
            raise AuthenticationFailed({
                "code": "INVALID_USER_DATA",
                "detail": "Données utilisateur incomplètes ou invalides."
            })

        # Vérifier ou créer l'utilisateur
        try:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'username': user_data['username'],
                    'first_name': user_data.get('first_name', ''),
                    'last_name': user_data.get('last_name', '')
                }
            )
            if created:
                logger.info(f"Nouvel utilisateur créé: {user.username}")
            else:
                logger.info(f"Utilisateur existant authentifié: {user.username}")

        except Exception as e:
            logger.critical(f"Erreur lors de la récupération/création de l'utilisateur: {e}")
            raise AuthenticationFailed({
                "code": "USER_CREATION_FAILED",
                "detail": "Impossible de créer ou récupérer l'utilisateur."
            })

        return (user, token)

    def authenticate_header(self, request):
        return 'Bearer'
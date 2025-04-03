---

# **📚 Plateforme de Gestion de Ressources, Événements et Système de Mentorat**


> **Plateforme complète pour la gestion des ressources de formation, des événements et des systèmes de mentorat.**  
> Elle permet de rechercher, filtrer, s'inscrire à des événements, et de participer à des sessions de mentorat.

---

## **🚀 Fonctionnalités Principales**
1. **Gestion des Ressources de Formation**  
   - Creation d'une ressource
   - Recherche et filtrage des ressources   

2. **Gestion du Calendrier des Événements**  
   - Liste et filtrage des événements pour la recherche
   - Inscription aux événements
   - Afficher les details d'un evenement 
   - Ajout d'événements au calendrier Google ou Outlook  personnel de l'utilisateur

3. **Système de Mentorat**  
   - Rechercher des mentors selon les informations de l'utilisateur
   - Recommandation de mentors adaptés  
   - Afficher les informations de mentorat
   - Suivi des progres de l'utilisateur dans le cadre du mentorat
   - Demander un mentora

---

## **🛠️ Technologies Utilisées**
- **Python 3.9+**  
- **Django 4.x** (Framework backend)  
- **Django REST Framework** (API REST)  
- **PostgreSQL** (Base de données)

---

## **📁 Structure du Projet**

```
my_project/
├── mentorship/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py  # Modèle Mentoring
│   ├── serializers.py  # Serializers des endpoints de mentorat
│   ├── views.py  # Vues des fonctionnalités de mentorat
│   └── urls.py  # Routes liées au mentorat
│
├── evenements/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py  # Modèle Event
│   ├── serializers.py  # Serializers des endpoints d'événements
│   ├── views.py  # Vues des fonctionnalités d'événements
│   └── urls.py  # Routes liées aux événements
│
├── formation/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py  # Modèle Resource
│   ├── serializers.py  # Serializers des endpoints de ressources
│   ├── views.py  # Vues des fonctionnalités de ressources
│   └── urls.py  # Routes liées aux ressources
│
├── my_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py  # Configuration du projet (DB, APPS)
│   ├── urls.py  # Fichier principal des routes
│   └── wsgi.py
│
└── manage.py  # Fichier de commande principal Django
```

---

## **📦 Installation**

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/ton-nom-utilisateur/nom-du-repo.git
   cd nom-du-repo
   ```

2. **Créer et activer un environnement virtuel**
   ```bash
   python -m venv env
   source env/bin/activate  # Sur Windows : .\env\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données**
   Modifiez `settings.py` pour ajouter les informations de votre base de données PostgreSQL :
   ```python
   DATABASES = {
       'default':
      dj_database_url.config(default='postgresql://rajapi:PpKxHkhRbt3Zj4lVrQI5foJWbIRMLrKo@dpg-cv2oeg5umphs739t27m0-a.oregon-postgres.render.com/bd_rajapi')
   }
   ```

5. **Effectuer les migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

7. **Lancer le serveur**
   ```bash
   python manage.py runserver
   ```

---

## **🛠️ Utilisation de l'API**

### **1. Gestion des Ressources de Formation**
| **Action**                | **Méthode**  | **Endpoint**              |
|--------------------------|-------------|---------------------------|
| Liste des ressources      | `GET`       | `/api/formation/`          |
| Créer une ressource       | `POST`      | `/api/formation/create/`   |

Pour voir la liste des evenements
GET /api/formation/
Authorization: Token VOTRE_TOKEN
```
Reponse:
{
   "id": 1,
    "Title": "Apprendre Django",
    "Description": "Formation complète sur Django REST Framework",
    "Type": "video",
    "File_Link": "https://example.com/django.mp4",
    "Published_Date": "2024-04-01",
    "Author_Id": 42,
    "Status": "published",
    "Created_At": "2024-04-01T12:00:00Z",
    "Update_At": "2024-04-01T12:00:00Z",
}
```

pour creer une ressource
Authorization: Token VOTRE_TOKEN
```
[
    {
        "Title": "Formation Django",
        "Description": "Vidéo",
        "Type": "Débutant",
        "File_Link": "https://www.youtube.com/watch?v=nI8xnkIn0_o&list=TLPQMDQwMzIwMjWrBloB3oS4-Q&index=2",
        "Published_Date": "2025-03-01",
        "Published_Date": "2025-03-01",
        "Status": "published",
        "Created_At":"2024-04-01T12:00:00Z",
        "Update_At": "2024-04-01T12:00:00Z"
    }
]
```

```
{
    "id": 1,
    "Title": "Apprendre Django",
    "Description": "Formation complète sur Django REST Framework",
    "Type": "video",
    "File_Link": "https://example.com/django.mp4",
    "Published_Date": "2024-04-01",
    "Author_Id": 42,
    "Status": "published",
    "Created_At": "2024-04-01T12:00:00Z",
    "Update_At": "2024-04-01T12:00:00Z",
    "author_info": {
        "id": 42,
        "username": "merlinb",
        "email": "merlinb@example.com",
        "first_name": "Merlin",
        "last_name": "Brice"
    }
}

```

---

### **2. Gestion des Événements**
| **Action**                 | **Méthode**  | **Endpoint**               |
|---------------------------|-------------|----------------------------|
| creer un evenements        |  `POST`     | ``/api/evenements/create/  |
| Recherche evenements       | `GET`       | `/api/evenements/`             |
| Détails d'un événement     | `GET`       | `/api/evenements/<id>/`        |
| Ajouter au calendrier      | `POST`      | `/api/eventements/<event_id>/calendar/` |

pour creer un evenement
Authorization: Token VOTRE_TOKEN
```
Body:
{
    "Title": "Conférence IA",
    "Description": "Une conférence sur l'IA et le Machine Learning.",
    "Start_Date_Time": "2024-04-10T10:00:00Z",
    "End_Date_Time": "2024-04-10T12:00:00Z",
    "Localisation": "Université de Yaoundé",
    "Participation_Link": "https://example.com/ia-conference",
    "Reminber_Set": "1 heure avant",
    "Summary": "Résumé de la conférence",
    "Timezone": "Africa/Douala",
    "Recurrence": "every week",
    "Attendees": "john@example.com, alice@example.com"
}
```

```
{
    "id": 1,
    "Title": "Conférence IA",
    "Description": "Une conférence sur l'IA et le Machine Learning.",
    "Start_Date_Time": "2024-04-10T10:00:00Z",
    "End_Date_Time": "2024-04-10T12:00:00Z",
    "Localisation": "Université de Yaoundé",
    "Participation_Link": "https://example.com/ia-conference",
    "Reminber_Set": "1 heure avant",
    "Summary": "Résumé de la conférence",
    "Timezone": "Africa/Douala",
    "Recurrence": "every week",
    "Attendees": "john@example.com, alice@example.com",
    "Created_At": "2024-04-01T12:00:00Z",
    "Updated_At": "2024-04-01T12:00:00Z",
    "Organized_By": 42,
    "organizer_info": {
        "id": 42,
        "username": "merlinb",
        "email": "merlinb@example.com",
        "first_name": "Merlin",
        "last_name": "Brice"
    }
}
```

POST /api/events/3/register/
Authorization: Token VOTRE_TOKEN

POST /api/events/3/calendar/
Authorization: Token VOTRE_TOKEN

---

### **3. Système de Mentorat**
| **Action**                     | **Méthode**  | **Endpoint**                     |
|---------------------------------|-------------|-----------------------------------|
| Introduction au mentorat        | `GET`       | `/api/mentorship/`                 |
| Recherche de mentors            | `GET`       | `/api/mentorship/search/`          |
| Recommandation de mentors       | `GET`       | `/api/mentorship/recommend/`       |
| Suivi des progrès du mentorat   | `GET`       | `/api/mentorship/progress/`        |
| Demande d'un mentorat           | `GET`       | `/api/mentorship/demande/`        |

GET /api/mentorship/search/?skills=gestion

GET /api/mentorship/progress/
Authorization: Token VOTRE_TOKEN

```
Reponse:
[
    {
        "id": 1,
        "username": "mentor_1",
        "email": "mentor1@example.com",
        "phone_number": "+237600000001",
        "is_verified": true
    },
    {
        "id": 2,
        "username": "mentor_2",
        "email": "mentor2@example.com",
        "phone_number": "+237600000002",
        "is_verified": true
    },
    {
        "id": 3,
        "username": "mentor_3",
        "email": "mentor3@example.com",
        "phone_number": "+237600000003",
        "is_verified": false
    },
    {
        "id": 4,
        "username": "mentor_4",
        "email": "mentor4@example.com",
        "phone_number": "+237600000004",
        "is_verified": true
    },
    {
        "id": 5,
        "username": "mentor_5",
        "email": "mentor5@example.com",
        "phone_number": "+237600000005",
        "is_verified": false
    }
]
```

GET /api/mentorship/progress/
Authorization: Token VOTRE_TOKEN
Reponse:
```
[
    {
        "mentee_info": {
            "id": 42,
            "username": "merlinb",
            "email": "merlinb@example.com",
            "first_name": "Merlin",
            "last_name": "Brice"
        },
        "mentor_info": {
            "id": 12,
            "username": "Mentor_12",
            "phone_number": "Non disponible",
            "is_verified": true
        },
        "Start_Date": "2024-04-10",
        "End_Date": "2024-06-10",
        "Status": "active",
        "Created_At": "2024-04-01T12:00:00Z",
        "Updated_At": "2024-04-01T12:00:00Z"
    }
]
```
reponse si mentorat pas trouve
```
{
    "message": "Aucune relation de mentorat active trouvée"
}
```

GET /api/mentorship/demande/
Authorization: Token VOTRE_TOKEN
```
Body:
{
    "Start_Date": "2024-04-10",
    "End_Date": "2024-06-10"
}
```

```
Reponse:
{
    "message": "Demande de mentorat créée avec succès",
    "mentoring": {
        "id": 12,
        "Start_Date": "2024-04-10",
        "End_Date": "2024-06-10",
        "Status": "active",
        "Created_At": "2024-04-01T12:00:00Z",
        "Updated_At": "2024-04-01T12:00:00Z",
        "mentee_info": {
            "id": 42,
            "username": "merlinb",
            "email": "merlinb@example.com",
            "first_name": "Merlin",
            "last_name": "Brice"
        },
        "mentor_id": 5
    }
}
```


---

## **✅ Tests**

**Exécuter les tests unitaires**
```bash
python manage.py test
```

---
--
-

## **🛠️ Améliorations Futures**
- Ajouter le support de **WebSockets** pour le chat en direct.  
- Ajouter des **notifications push** pour les rappels d'événements.  
- Améliorer l'interface utilisateur avec **Django Templates** ou **React.js**.  

---

## **📞 Support**
Pour toute question ou assistance, contactez **MBASSI ATANGANA**. 

---

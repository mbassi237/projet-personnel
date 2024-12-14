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
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'nom_de_la_base',
           'USER': 'utilisateur',
           'PASSWORD': 'mot_de_passe',
           'HOST': 'localhost',
           'PORT': '5432',
       }
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

---

### **2. Gestion des Événements**
| **Action**                 | **Méthode**  | **Endpoint**               |
|---------------------------|-------------|----------------------------|
| Recherche evenements       | `GET`       | `/api/evenements/`             |
| Détails d'un événement     | `GET`       | `/api/evenements/<id>/`        |
| Ajouter au calendrier      | `POST`      | `/api/eventements/<event_id>/calendar/` |

---

### **3. Système de Mentorat**
| **Action**                     | **Méthode**  | **Endpoint**                     |
|---------------------------------|-------------|-----------------------------------|
| Introduction au mentorat        | `GET`       | `/api/mentorship/mentoring-introduction`                 |
| Recherche de mentors            | `GET`       | `/api/mentorship/mentor-search/`          |
| Recommandation de mentors       | `GET`       | `/api/mentorship/mentor-recommendation/`       |
| Suivi des progrès du mentorat   | `GET`       | `/api/mentorship/progress/`        |

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

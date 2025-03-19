# Détection du Paludisme à l'aide d'Images de Frottis Sanguin

Ce projet est une application Django permettant l'enregistrement des patients et l'analyse d'images de frottis sanguin pour détecter la présence du paludisme en utilisant un modèle CNN. L'application génère également un rapport PDF des résultats.

## Prérequis

Avant de lancer le projet, assurez-vous d'avoir les éléments suivants installés :

- Python 3.x
- Django
- Django REST Framework
- TensorFlow / Keras
- pillow
- ReportLab

## Installation

1. Clonez le dépôt GitHub :

```bash
    git clone https://github.com/votre-utilisateur/votre-repo.git
```

2. Accédez au répertoire du projet :

```bash
    cd votre-repo
```

3. Installez les dépendances requises :

```bash
    pip install -r requirements.txt
```

4. Appliquez les migrations de la base de données :

```bash
    python manage.py migrate
```

5. Démarrez le serveur Django :

```bash
    python manage.py runserver
```

## Endpoints de l'API

### 1. Enregistrement d'un patient

**URL:** `https://projet-personnel.onrender.com/api/patients/`

**Méthodes:** `POST`

**Description:**
- Affiche un formulaire pour enregistrer un patient.
- Enregistre un nouveau patient avec un code unique généré automatiquement.

**Exemple de requête (POST)** :

```bash
    curl -X POST https://projet-personnel.onrender.com/api/patients/ \
    -d "nom=Jean Doe" \
    -d "sexe=Masculin" \
    -d "age=30" \
    -d "email=jean.doe@example.com"
```

**Réponse attendue (JSON)** :

```json
    { "reponse": "patient bien enregistré" }
```

---

### 2. Analyse d'un frottis sanguin

**URL:** `https://projet-personnel.onrender.com/api/analysefrottis/`

**Méthodes:** `POST`

**Description:**
-Selectionner un patient
- Charge l'image d'un frottis sanguin du patient.
- Exécute une analyse via un modèle CNN .
- Met à jour la base de données avec le statut du frottis.

**Exemple de requête (POST)** :

```bash
    curl -X POST https://projet-personnel.onrender.com/api/analysefrottis/ \
    -F "id_patient=1" \
    -F "image=@path_to_frottis_image.jpg"
```

**Réponse attendue (HTML rendue)** :
L'utilisateur est redirigé vers la page affichant les résultats d'analyse.

---

### 3. Génération d'un rapport d'analyse

**URL:** `https://projet-personnel.onrender.com/api/rapportpdf/`

**Méthodes:** `POST`

**Description:**
- Génère un rapport PDF basé sur les reultats obtenus de l'analyse de frottis sanguin analysé du patient.
- Télécharge le rapport contenant les informations du patient et les résultats de l'analyse.

**Exemple de requête (POST)** :

```bash
    curl -X POST https://projet-personnel.onrender.com/api/rapportpdf/ \
    -H "Content-Type: application/json" \
    -d '{"id_patient": 1}'
```

**Réponse attendue:**
Un fichier PDF contenant le rapport de l'analyse du patient qui est telecharge.

---

## Structure du Projet

```
📂 projet-personnel
 ├── 📂 doameki/
 │   ├── views.py
 │   ├── models.py
 │   ├── serializers.py
 │   ├── urls.py
 ├── manage.py
 ├── requirements.txt
 ├── README.md
```

## Améliorations futures

- Implémentation d'une interface utilisateur interactive.
- Amélioration du modèle de détection du paludisme.
- Stockage et visualisation des tendances des résultats des patients.

## Auteur
MBASSI ATANGANA

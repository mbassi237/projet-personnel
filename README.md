# Systeme de Mentorat API - Documentation

Bienvenue dans la documentation de l'API REST du système de mentorat.
Cette API permet de gérer les relations entre mentorés et mentors, demande de mentor, envoie message liste des messages liste des mentoring et la progression du mentorat.

---

## 🔑 Authentification

**Endpoint :**
```http
POST https://rajapi-cop-auth-api.onrender.com/auth/token/
```

**Body :**
```json
{
  "username": "owner",
  "password": "Pass123!@"
}
```

**Réponse :**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MzkzOTg3NSwiaWF0IjoxNzQzODUzNDc1LCJqdGkiOiJlZDkzNjIwN2U5NTU0Yzk1YjBkZWU3ZDY2MjkyYTY1NyIsInVzZXJfaWQiOjF9.vrIZR9oQylradfSr7K_ZqPdluczyHL4D9Xol5Ov1ryw",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQzODUzNzc1LCJpYXQiOjE3NDM4NTM0NzUsImp0aSI6IjFkMTg2ZGMxNDJkMTQ3MTI5ZDBmNjgxMjZiZjlhZTk3IiwidXNlcl9pZCI6MX0.j1lVry_W6NIxF4m2nOwymkYiPSagjakJ1JYGcntROHQ"
}
```

Utilisez le token d'accès dans l'en-tête :
```http
Authorization: Bearer <access_token>
```

---

## 📊 Voir la progression du mentorat

**GET** `https://systemementorat.onrender.com/api/mentorship/progress/`

**Réponse :**
```json
[
  {
    "mentee_info": {
      "id": 1,
      "username": "owner",
      "email": "ll@rajapi.com",
      "first_name": "Project",
      "last_name": "Owner"
    },
    "mentor_info": {
      "id": 2,
      "username": "Mentor_2",
      "phone_number": "Non disponible",
      "is_verified": true
    },
    "Start_Date": "2024-01-01",
    "End_Date": "2024-12-31",
    "Status": "active",
    "Created_At": "2025-04-11T12:58:43.959579Z",
    "Updated_At": "2025-04-11T12:58:43.959579Z"
  }
]
```

---

## 💬 Discussion (Chat) entre mentor et mentoré

**GET** `https://systemementorat.onrender.com/api/mentoring/chat/<mentoring_id>/messages/`

**Réponse :**
```json
[
  {
    "id": 1,
    "sender_id": "1",
    "message": "Bonjour, comment puis-je vous aider ?",
    "created_at": "2025-04-11T12:02:13.135423Z"
  },
  {
    "id": 2,
    "sender_id": "1",
    "message": "Bonjour, je suis prêt à commencer ! pour une nouvelle aventure dans l'etude du climat",
    "created_at": "2025-04-11T16:00:05.079044Z"
  }
]
```

**POST** `https://systemementorat.onrender.com/api/mentoring/chat/<mentoring_id>/messages/`

**Body :**
```json
{
  "message": "Bonjour, j'aimerais qu'on entre en contact pour un mentorat pour mon expose sur l'environnement."
}
```

**Réponse :**
```json
{
  "id": 3,
  "message": "Bonjour, j'aimerais qu'on entre en contact pour un mentorat pour mon expose sur l'environnement."
}
```

---

## 🧑‍🏫 Créer une demande de mentorat

**POST** `https://systemementorat.onrender.com/api/mentorship/demande/`

**Body :**
```json
{
  "mentor_id": 5,
  "mentee_id": 2,
  "Start_Date": "2025-01-01",
  "End_Date": "2025-12-31"
}
```

**Réponse :**
```json
{
  "mentor_id": 5,
  "mentee_id": 1,
  "Status": "active",
  "Start_Date": "2025-01-01",
  "End_Date": "2025-12-31"
}
```

---

## 📝 Voir toutes les demandes de mentorat

**GET** `https://systemementorat.onrender.com/api/mentorship/demande/`

**Réponse :**
```json
[
  {
    "mentor_id": 123,
    "mentee_id": 1,
    "Status": "active",
    "Start_Date": "2024-01-01",
    "End_Date": "2024-12-31"
  },
  {
    "mentor_id": 1,
    "mentee_id": 1,
    "Status": "inactive",
    "Start_Date": "2025-04-10",
    "End_Date": "2025-04-12"
  },
  {
    "mentor_id": 5,
    "mentee_id": 1,
    "Status": "active",
    "Start_Date": "2025-01-01",
    "End_Date": "2025-12-31"
  }
]
```

---

## 👤 Valider ou refuser une demande de mentorat

**PATCH** `https://systemementorat.onrender.com/api/mentoring/requests/<request_id>/respond/`

**Body :**
```json
{
  "status": "active"
}
```

**Réponse :**
```json
{
  "mentor_id": 1,
  "mentee_id": 1,
  "Status": "active",
  "Start_Date": "2025-04-10",
  "End_Date": "2025-04-12"
}
```

---

## 🔍 Voir tous les mentorings de l'utilisateur

**GET** `https://systemementorat.onrender.com/api/mentoring/`

**Réponse :**
```json
[
  {
    "mentor_id": 1,
    "mentee_id": 1,
    "Status": "inactive",
    "Start_Date": "2025-04-10",
    "End_Date": "2025-04-12"
  },
  {
    "mentor_id": 123,
    "mentee_id": 1,
    "Status": "active",
    "Start_Date": "2024-01-01",
    "End_Date": "2024-12-31"
  }
]
```

---

## 🌐 Déploiement

Le projet est déployé sur render :
```
https://systemementorat.onrender.com
```

Utilisez un outil comme Postman ou `curl` pour tester les routes avec les tokens JWT obtenus via le microservice d'authentification.

---

Pour toute question, contacte `yannickserge.escobar@gmail.com`


from django.db import models

# Create your models here.


class Mentor(models.Model):
    Nom_mentor = models.CharField(max_length=30)
    Prenom_mentor = models.CharField(max_length=30)
    Profession = models.CharField(max_length=30)
    LastConnected = models.DateField(auto_now_add=True)



class Mentoring(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    Mentor_Id = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    #Mentee_Id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mentorships_as_mentee')
    #mentor_id = models.IntegerField()
    mentee_id = models.IntegerField()
    Start_Date = models.DateField()
    End_Date = models.DateField()
    Status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)

class MentoringMessage(models.Model):
    mentoring = models.ForeignKey(Mentoring, on_delete=models.CASCADE, related_name='messages')
    sender_id = models.CharField(max_length=255)  # UUID ou email de l'expéditeur
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
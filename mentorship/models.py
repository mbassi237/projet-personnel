from django.db import models
from user.models import CustomUser
# Create your models here.

class Mentoring(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    Mentor_Id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mentorships_as_mentor')
    Mentee_Id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mentorships_as_mentee')
    Start_Date = models.DateField()
    End_Date = models.DateField()
    Status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)
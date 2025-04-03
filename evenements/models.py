#from user.models import CustomUser
from django.db import models

# Create your models here.

class Events(models.Model):
    RECCURENCES_CHOICES = [
        ('every week', 'Every Week'),
        ('every monday', 'Every Monday'),
    ]
    Title = models.CharField(max_length=50)
    Description = models.TextField()
    Start_Date_Time = models.DateTimeField()
    End_Date_Time = models.DateTimeField()
    Localisation = models.CharField(max_length=255, null=True, blank=True)
    #Organized_By = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Participation_Link = models.URLField(max_length=255, null=True, blank=True)
    Reminber_Set = models.CharField(max_length=255, null=True, blank=True)
    Summary = models.CharField(max_length=255, null=True, blank=True)
    Timezone = models.CharField(max_length=25)
    Recurrence = models.CharField(max_length=100, null=True, choices=RECCURENCES_CHOICES, default='every week')
    Attendees =models.TextField()
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.Title} ({self.Title})"
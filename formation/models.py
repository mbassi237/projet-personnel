from django.db import models

from user.models import CustomUser


# Create your models here.


class Ressources(models.Model):
    RESSOURCE_TYPES = [
        ('audio', 'Audio'),
        ('document', 'Document'),
        ('video', 'Video'),
    ]
    STATUS_CHOICES = [
        ('drafted', 'Drafted'),
        ('published', 'Published'),
    ]

    Title = models.CharField(max_length=100)
    Description = models.TextField()
    Type = models.CharField(max_length=50, choices=RESSOURCE_TYPES)
    File_Link = models.URLField(max_length=255)
    Published_Date = models.DateField()
    Author_Id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='drafted')
    Created_At = models.DateTimeField(auto_now_add=True)
    Update_At = models.DateTimeField(auto_now=True)


class Formation(models.Model):
    STATUS_CHOICES = [
        ('published', 'Published'),
        ('archived', 'Archived'),
        ('drafted', 'Drafted'),
    ]
    Title = models.CharField(max_length=100)
    Description = models.TextField()
    Type = models.CharField(max_length=100)
    Created_By = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Content_Link = models.URLField(max_length=255)
    Duration = models.CharField(max_length=50)
    Status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='drafted')
    Created_At = models.DateTimeField(auto_now_add=True)
    Update_At = models.DateTimeField(auto_now=True)


class Formation_Content(models.Model):
    CONTENT_TYPES = [
        ('video', 'Video'),
        ('quiz', 'Quiz'),
        ('document', 'Document'),
    ]

    Formation_Id = models.ForeignKey(Formation, on_delete=models.CASCADE)
    Content_Type = models.CharField(max_length=50, choices=CONTENT_TYPES)
    Content_Link = models.URLField(max_length=100)
    Description = models.TextField()
    Duration = models.CharField(max_length=50)
    Order = models.PositiveIntegerField()
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', "ADMIN"),
        ('member', "MEMBER"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    newsletter_subscription = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    # Ajout des related_name pour éviter les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Ajoutez related_name ici pour eviter les conflits
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Ajoutez related_name ici
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    def __str__(self):
        return self.username

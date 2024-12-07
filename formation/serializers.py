
from rest_framework import serializers
from .models import Ressources

class RessourceSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), required=False) # Ajout des tags thematique

    class Meta:
        model = Ressources
        fields = '__all__'
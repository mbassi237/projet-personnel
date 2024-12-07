
from rest_framework import serializers
from .models import Mentoring

class MentoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentoring
        fields = '__all__'
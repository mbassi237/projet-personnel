from rest_framework import serializers 
from .models import Patient, Frottis, Rapport


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'



class FrottisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frottis
        fields = '__all__'
        extra_kwargs = {'status': {'required': False}}



class RapportSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Rapport
        fields = '__all__'
from rest_framework import serializers
from .models import Mentoring, MentoringMessage, Mentor


class MentoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentoring
        fields = '__all__'




class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'


class MentoringMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentoringMessage
        fields = ['id', 'sender_id', 'message', 'created_at']
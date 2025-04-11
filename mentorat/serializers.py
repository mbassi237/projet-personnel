from rest_framework import serializers
from .models import Mentoring, MentoringMessage

class MentoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentoring
        fields = ['mentor_id', 'mentee_id', 'Status', 'Start_Date', 'End_Date']



class MentoringMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentoringMessage
        fields = ['id', 'sender_id', 'message', 'created_at']
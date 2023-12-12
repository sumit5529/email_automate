
from rest_framework import serializers

from .models import Subscriber,EmailHistory,EmailPlusScheduleModel

class subscriber_serializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    email_count = serializers.SerializerMethodField(read_only=True)
    def get_email_count(self,subscriber):
        count = EmailPlusScheduleModel.objects.filter(subscriber=subscriber).count()
        return count
    class Meta:
        model = Subscriber
        fields = '__all__'
        

class email_plus_schedule_serializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    subscriber = subscriber_serializer()
    
    class Meta:
        model = EmailPlusScheduleModel
        fields = '__all__'
        

class email_history_serializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    subscriber = subscriber_serializer()
    
    class Meta:
        model = EmailHistory
        fields = '__all__'
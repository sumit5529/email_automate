
from rest_framework import serializers

from .models import Subscriber,EmailHistory,EmailPlusScheduleModel
"""Api of subscriber with content of username and EmailHistory"""
class SubscriberSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    email_count = serializers.SerializerMethodField(read_only=True)
    def get_email_count(self,subscriber):
        count = EmailPlusScheduleModel.objects.filter(subscriber=subscriber).count()
        return count
    class Meta:
        model = Subscriber
        fields = '__all__'
        
""" For providing api to frontend of Email content , schedule time,periodicity and gap"""
class EmailPlusScheduleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    subscriber = SubscriberSerializer()
    
    class Meta:
        model = EmailPlusScheduleModel
        fields = '__all__'
        
""" For providing api to frontend  of sent Email (History)"""
class EmailHistorySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    subscriber = SubscriberSerializer()
    
    class Meta:
        model = EmailHistory
        fields = '__all__'
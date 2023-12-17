# forms.py

from django import forms
from .models import Subscriber,EmailPlusScheduleModel
from django.contrib.admin.widgets import AdminDateWidget


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['name', 'email']
class EmailplusScheduleForm(forms.ModelForm):
    class Meta:
        model = EmailPlusScheduleModel
        fields = ['subject','message_text','schedule_time','gp','frequency','status']


        widgets = {
        
      
         'schedule_time': forms.DateTimeInput(attrs={'class':'form-control','type': 'datetime-local'}),
     
         'subject': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
         
         'message_text': forms.Textarea(attrs={'rows': 7, 'cols': 30}),
         'gp' : forms.TextInput(attrs={'placeholder': 'HH:MM:SS'})
        #   'gp': forms.TextInput(attrs = {'placeholder':'gap in minutes'})
         
     
        
      
        }

















# forms.py

from django import forms
from .models import Subscriber,EmailModel,NextEmailHistory,EmailPlusScheduleModel
from django.contrib.admin.widgets import AdminDateWidget


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['name', 'email']


class EmailForm(forms.Form):
    #  class Meta:
    #     model = NextEmailHistory
    #     fields = ['schedule_date','schedule_time','periodic_gap_day']
    #     widgets = {
    #         'schedule_date': forms.DateInput(
    #             attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'}
    #         ),
    #         'schedule_time': forms.TimeInput(
    #             attrs={'type': 'time', 'placeholder': 'HH-MM-SS', 'class': 'form-control'}
    #         )
    #     }
    # subject = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))
    # message_text = forms.CharField(widget=forms.Textarea)
    schedule_date = forms.DateField(
        label='Enter Date',
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']  # Adjust format as per your requirement
    )
    
    schedule_time = forms.TimeField(
        label='Enter Time',
        widget=forms.widgets.TimeInput(attrs={'type': 'time'}),
        input_formats=['%H:%M:%S']  
    ) 
    periodic_gap_day = forms.IntegerField()


class EmailContentForm(forms.ModelForm):
    class Meta:
        model = EmailModel
        fields = '__all__'  



    
    widgets = {
        'subject': forms.TextInput(attrs={'rows': 2, 'cols': 20}),
        'message_text': forms.Textarea(attrs={'rows': 5, 'cols': 20}),
      
    }

# class EmailIndividualForm(forms.ModelForm):
#     class Meta:
#         model = Subscriber
#         fields = ['subject', 'message_text']



class EmailplusScheduleForm(forms.ModelForm):
    class Meta:
        model = EmailPlusScheduleModel
        fields = ['subject','message_text','schedule_time','gap','frequency']


        widgets = {
        # 'subject': forms.TextInput(attrs={'rows': 2, 'cols': 20}),
        # 'message_text': forms.Textarea(attrs={'rows': 5, 'cols': 20}),
      
         'schedule_time': forms.DateTimeInput(attrs={'class':'form-control','type': 'datetime-local'}),
     

         
         'message_text': forms.Textarea(attrs={'rows': 5, 'cols': 20}),
         
     
        
      
        }




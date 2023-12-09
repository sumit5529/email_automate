from django.db import models
from django.utils import timezone
# Create your models here.
# models.py


class Subscriber(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # subject = models.CharField(max_length=255,default="subject")
    # message_text = models.CharField(max_length=255,default="text")

   

    def __str__(self):
        return self.name
    

class EmailHistory(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    sender = models.EmailField()
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subscriber.name
    
class NextEmailHistory(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    schedule_date = models.DateField(
        
        # label='Enter Date',
        # widget=models.widgets.DateInput(attrs={'type': 'date'}),
        # input_formats=['%Y-%m-%d']  # Adjust format as per your requirement
       
    )
    
    schedule_time = models.TimeField(
       default=timezone.localtime(timezone.now()).time()
        # label='Enter Time',
        # widget=models.widgets.TimeInput(attrs={'type': 'time'}),
        # input_formats=['%H:%M']  
    ) 
    periodic_gap_day = models.IntegerField()



class EmailModel(models.Model):
    subject = models.CharField(max_length=255)
    message_text = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and EmailModel.objects.exists():
            # Update existing instance
            existing_instance = EmailModel.objects.first()
            existing_instance.subject = self.subject
            existing_instance.message_text = self.message_text
            existing_instance.save()
            return existing_instance

        # Save as usual for a new instance
        super(EmailModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.subject
    


class EmailPlusScheduleModel(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255,default="subject")
    message_text = models.CharField(max_length=255,default="text")
    # schedule_time = models.models.DateTimeField(default=timezone.localtime(timezone.now()).time())
    schedule_time = models.DateTimeField()
    gap = models.IntegerField()
    frequency = models.IntegerField()

    def __str__(self):
        return self.subject + str(self.gap)
    
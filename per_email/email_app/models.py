from django.db import models
from django.utils import timezone


"""Model of subscriber"""
class Subscriber(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.name
    
""" After sending email with below field,history of that user will get saved"""
class EmailHistory(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    sender = models.EmailField()
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subscriber.name
    
    # @classmethod
    # def create_email_history(cls, subscriber, sender, recipient, subject, body):
    #     """
    #     Create an EmailHistory object and save it to the database.

    #     Parameters:
    #     - subscriber: Subscriber instance (foreign key)
    #     - sender: Email address of the sender
    #     - recipient: Email address of the recipient
    #     - subject: Subject of the email
    #     - body: Body/content of the email

    #     Returns:
    #     - EmailHistory instance
    #     """
    #     email_history = cls(
    #         subscriber=subscriber,
    #         sender=sender,
    #         recipient=recipient,
    #         subject=subject,
    #         body=body
    #     )
    #     email_history.save()
    #     # return email_history
    





    

"""For storing scheduling  time and email content"""
class EmailPlusScheduleModel(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255,default="subject")
    message_text = models.CharField(max_length=255,default="text")
    # schedule_time = models.models.DateTimeField(default=timezone.localtime(timezone.now()).time())
    schedule_time = models.DateTimeField()
    gp= models.DurationField()
    frequency = models.IntegerField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.subject + str(self.gp)
    

























    
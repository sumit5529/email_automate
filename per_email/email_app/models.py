from django.db import models

# Create your models here.
# models.py


class Subscriber(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=255,default="subject")
    message_text = models.CharField(max_length=255,default="text")

   

    def __str__(self):
        return self.name


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
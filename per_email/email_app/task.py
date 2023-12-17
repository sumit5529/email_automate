# your_app/tasks.py







from celery import Celery
from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import Subscriber,EmailHistory,EmailPlusScheduleModel
from django.conf import settings
from celery.schedules import crontab
from celery.result import AsyncResult
import json
from django.utils import timezone
from datetime import timedelta
import logging
import asyncio
from django.db.models import Q




# app = Celery('per_email', broker='pyamqp://guest@localhost//')

logger = logging.getLogger(__name__)



@shared_task
def checkschedule():
    try:
        
        current_datetime = datetime.now()


        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")

        all_email = EmailPlusScheduleModel.objects.filter(Q(schedule_time__lte=formatted_datetime) & Q(status=True))
        # all_email.update(status = False)
        for each_email in all_email:
            each_email.status = False
        if all_email.exists():
            # print(all_email.status)
            logger.info('Processing scheduled emails')
            process_scheduled_emails(all_email)
        else:
            logger.info('No scheduled emails at the moment')

    except Exception as e:
        logger.error(f"Error in checkschedule task: {str(e)}")



def process_scheduled_emails(emails):
    for each_email in emails:
        try:
            print(each_email.status)
            send_email(each_email)
            save_email_history(each_email)
            update_email_schedule(each_email)
        except Exception as e:
            logger.error(f"Error processing email: {str(e)}")


def send_email(email):
    subject = email.subject
    message_text = email.message_text
    recipient_list = [email.subscriber.email,]
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message_text, from_email, recipient_list)
    logger.info(f"Email sent to {email.subscriber.email}")


def save_email_history(email):
    EmailHistory.objects.create(
        subscriber=email.subscriber,
        sender=settings.EMAIL_HOST_USER,
        recipient=email.subscriber.email,
        subject=email.subject,
        body=email.message_text
    )
    # print('email history saved')


def update_email_schedule(email):
    frequency = email.frequency - 1

    if frequency == 0:
        email.delete()
    else:
        gp = email.gp
        # email.schedule_time = timezone.localtime(timezone.now() + timedelta(minutes=gap))
        email.schedule_time = email.schedule_time + email.gp
        email.frequency = frequency
        email.status = True
        email.save()

        # print('email updated')

         





      
      
   
  


























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





app = Celery('per_email', broker='pyamqp://guest@localhost//')

logger = logging.getLogger(__name__)



@shared_task
def checkschedule():
    try:
        # current_time = timezone.localtime(timezone.now()).time()
        # logger.info(f"Current time: {current_time}")
        current_datetime = datetime.now()


        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")

        all_email = EmailPlusScheduleModel.objects.filter(schedule_time__lte=formatted_datetime)

        if all_email.exists():
            logger.info('Processing scheduled emails')
            process_scheduled_emails(all_email)
        else:
            logger.info('No scheduled emails at the moment')

    except Exception as e:
        logger.error(f"Error in checkschedule task: {str(e)}")


def process_scheduled_emails(emails):
    for each_email in emails:
        try:
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
    print('email history saved')


def update_email_schedule(email):
    frequency = email.frequency - 1

    if frequency == 0:
        email.delete()
    else:
        gap = email.gap
        # email.schedule_time = timezone.localtime(timezone.now() + timedelta(minutes=gap))
        email.schedule_time = email.schedule_time + timedelta(hours=gap)
        email.frequency = frequency
        email.save()

    print('email updated')

         





      
      
   
  



























   
# @shared_task
# def send_weekly_email():
    # subject = 'Your Weekly Update'
   #  message = message_text
    # print(subject, message)
    # tr = 'ram'
    # subscribers = Subscriber.objects.all()
    # emailobj= EmailModel.objects.all().first()
            
    # subj = emailobj.subject
    # message = emailobj.message_text
    
    # from_email = settings.EMAIL_HOST_USER
   

    # for subs in subscribers:
       
    #    print(subs.email)
    #    user_id = subs.id
    #    subsobj = Subscriber.objects.get(pk=user_id)
    # # Your task logic here
      
    #    EmailHistory.objects.create(
    #         subscriber=subsobj,
    #         sender=from_email,
    #         recipient=subsobj.email,
    #         subject=subsobj.subject,
    #         body=subsobj.message_text
    #      )
    #    recipient_list = [subs.email,]

    #    send_mail(subj, message, from_email, recipient_list)

   # Define periodic task
   #  app.conf.beat_schedule['send-weekly-email']['schedule'] = crontab(minute=2)
   #  solve(periodic_gap_day)

   
    # return "done"
    # pass

# @shared_task
# def individual_periodic_task(user_id):
    # subsobj = Subscriber.objects.get(pk=user_id)
    # # Your task logic here
	

    
    # from_email = settings.EMAIL_HOST_USER
    # EmailHistory.objects.create(
    #         subscriber=subsobj,
    #         sender=from_email,
    #         recipient=subsobj.email,
    #         subject=subsobj.subject,
    #         body=subsobj.message_text
    #     )
    # # subscriber = Subscriber.objects.get(id = user_id)
    # emailobj = NextEmailHistory.objects.filter(subscriber=subsobj).first()
    # recipient_list = [subsobj.email,]
     
    # send_mail(subsobj.subject,subsobj.message_text,from_email,recipient_list)
    # gap = emailobj.periodic_gap_day
    # emailobj.schedule_time =  timezone.localtime(timezone.now() + timedelta(seconds=gap))
    
    # emailobj.save()
    # pass
    
    
    
   


# def individual_gap(primary_key,gap):
#   try:
      
#     existing_task = PeriodicTask.objects.get(name=f"Your Periodic Task{primary_key}")
#     new_interval, created = IntervalSchedule.objects.get_or_create(
#     every=gap,
#     period=IntervalSchedule.SECONDS,)
#     existing_task.interval = new_interval
#     existing_task.enabled = True
#     existing_task.args = [primary_key]
#     # existing_task.enable_task()
#     existing_task.save()
#   except PeriodicTask.DoesNotExist:
   
      
  


    
#     interval_schedule, created = IntervalSchedule.objects.get_or_create(
#     every=gap,
#     period=IntervalSchedule.SECONDS,)


#     periodic_task = PeriodicTask.objects.create(
    
#     name=f'Your Periodic Task{primary_key}',
#     task='email_app.task.individual_periodic_task',  
#     # args= [primary_key],
#     # args = json.dumps(["{primary_key}"]),
#     args = [primary_key],
#     interval=interval_schedule,
#     )
#     periodic_task.enabled = True
    # periodic_task.enable_task()
    # pass

# @shared_task
# def checkschedule():
#    current_time = timezone.localtime(timezone.now()).time()
#    print(current_time)
#    all_email = EmailPlusScheduleModel.objects.filter(schedule_time__lte=current_time)
#    if all_email:
#        print('ok')
#    else:
#        print ('not ok')
#    for eachemail in all_email:
#       subscriber = eachemail.subscriber
#       subject = eachemail.subject
#       message_text = eachemail.message_text
#       gap = eachemail.gap
#       schedule_time = eachemail.schedule_time
#       recipient_list = [subscriber.email,]
#       from_email = settings.EMAIL_HOST_USER
#       send_mail(subject,message_text,from_email,recipient_list)
#       print('email has been  sent to)
#       EmailHistory.objects.create(
#             subscriber=subscriber,
#             sender=from_email,
#             recipient=subscriber.email,
#             subject=subject,
#             body=message_text
#         )
#       frequecny = frequecny-1;
#       if(frequecny==0):
         
#          eachemail.delete()
#       else:
#         eachemail.schedule_time = timezone.localtime(timezone.now() + timedelta(minutes=gap))
#         eachemail.frequency = frequecny
#         eachemail.save()


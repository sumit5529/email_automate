# your_app/tasks.py
from celery import Celery
from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import Subscriber,EmailModel,EmailHistory,NextEmailHistory
from django.conf import settings
from celery.schedules import crontab
from celery.result import AsyncResult
import json
from django.utils import timezone
from datetime import timedelta


from django_celery_beat.models import PeriodicTask, IntervalSchedule


app = Celery('per_email', broker='pyamqp://guest@localhost//')


from celery.result import AsyncResult, allow_join_result
from celery.exceptions import SoftTimeLimitExceeded


def revoke_old_tasks():
    try:
        with allow_join_result():
            with app.timelimit(soft=120):  # Set the time limit to 2 minutes (120 seconds)
                print('Revoke')
                subscribers = Subscriber.objects.all()

                # Revoke each old task
                print('going revoke')
                for subs in subscribers:
                    task_id = subs.id  # Assuming 'id' is the task ID
                    result = AsyncResult(task_id)

                    # Check the task state before revoking
                    print(f'Task {task_id} state before revocation: {result.state}')

                    # Revoke the task
                    result.revoke(terminate=True)

                    # Check the task state after revocation
                    print(f'Task {task_id} state after revocation: {result.state}')
                print('revoked')

    except SoftTimeLimitExceeded:
        print('Operation exceeded the soft time limit. Some tasks might not have been revoked.')




   
@shared_task
def send_weekly_email():
    # subject = 'Your Weekly Update'
   #  message = message_text
    # print(subject, message)
    tr = 'ram'
    subscribers = Subscriber.objects.all()
    emailobj= EmailModel.objects.all().first()
            
    subj = emailobj.subject
    message = emailobj.message_text
    
    from_email = settings.EMAIL_HOST_USER
   

    for subs in subscribers:
       
       print(subs.email)
       user_id = subs.id
       subsobj = Subscriber.objects.get(pk=user_id)
    # Your task logic here
      
       EmailHistory.objects.create(
            subscriber=subsobj,
            sender=from_email,
            recipient=subsobj.email,
            subject=subsobj.subject,
            body=subsobj.message_text
         )
       recipient_list = [subs.email,]

       send_mail(subj, message, from_email, recipient_list)

   # Define periodic task
   #  app.conf.beat_schedule['send-weekly-email']['schedule'] = crontab(minute=2)
   #  solve(periodic_gap_day)

   
    return "done"

@shared_task
def individual_periodic_task(user_id):
    subsobj = Subscriber.objects.get(pk=user_id)
    # Your task logic here
	

    
    from_email = settings.EMAIL_HOST_USER
    EmailHistory.objects.create(
            subscriber=subsobj,
            sender=from_email,
            recipient=subsobj.email,
            subject=subsobj.subject,
            body=subsobj.message_text
        )
    # subscriber = Subscriber.objects.get(id = user_id)
    emailobj = NextEmailHistory.objects.filter(subscriber=subsobj).first()
    recipient_list = [subsobj.email,]
     
    send_mail(subsobj.subject,subsobj.message_text,from_email,recipient_list)
    gap = emailobj.periodic_gap_day
    emailobj.schedule_time =  timezone.localtime(timezone.now() + timedelta(seconds=gap))
    
    emailobj.save()
    
    
    
   


def individual_gap(primary_key,gap):
  try:
      
    existing_task = PeriodicTask.objects.get(name=f"Your Periodic Task{primary_key}")
    new_interval, created = IntervalSchedule.objects.get_or_create(
    every=gap,
    period=IntervalSchedule.SECONDS,)
    existing_task.interval = new_interval
    existing_task.enabled = True
    existing_task.args = [primary_key]
    # existing_task.enable_task()
    existing_task.save()
  except PeriodicTask.DoesNotExist:
   
      
  


    
    interval_schedule, created = IntervalSchedule.objects.get_or_create(
    every=gap,
    period=IntervalSchedule.SECONDS,)


    periodic_task = PeriodicTask.objects.create(
    
    name=f'Your Periodic Task{primary_key}',
    task='email_app.task.individual_periodic_task',  
    # args= [primary_key],
    # args = json.dumps(["{primary_key}"]),
    args = [primary_key],
    interval=interval_schedule,
    )
    periodic_task.enabled = True
    # periodic_task.enable_task()
  

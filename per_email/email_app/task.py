# your_app/tasks.py
from celery import Celery
from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import Subscriber,EmailModel
from django.conf import settings
from celery.schedules import crontab
from celery.result import AsyncResult
import json

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
       recipient_list = [subs.email,]

       send_mail(subj, message, from_email, recipient_list)

   # Define periodic task
   #  app.conf.beat_schedule['send-weekly-email']['schedule'] = crontab(minute=2)
   #  solve(periodic_gap_day)

   
    return "done"

@shared_task
def individual_periodic_task(user_id):
    user = Subscriber.objects.get(pk=user_id)
    # Your task logic here
    print(f"Executing task for user {user_id}")


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
  

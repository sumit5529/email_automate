# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'per_email.settings')

app = Celery('per_email')
app.conf.enable_utc = False
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# def individual_gap(primary_key):
#     app.conf.beat_schedule['individual-periodic-task']['args'] = (primary_key,)
#     app.conf.beat_schedule['individual-periodic-task']['schedule'] = crontab(minute = "*/2")

# Define periodic task
app.conf.beat_schedule = {
    'send-weekly-email': {
        'task': 'email_app.task.send_weekly_email',
        'schedule': crontab(minute="*/5")
        # 'args':('subject','message_text')
        
    },
    'individual-periodic-task':{
        'task':'email_app.task.individual_periodic_task',
        'schedule': crontab(minute="*/4"),
        'args':(2,)
    }
}

def set_gap(periodic_gap_day):
    print('called solve')
    periodic_gap_time = int(periodic_gap_day)
    print(type(periodic_gap_day))
 
    x = f"*/{periodic_gap_time}"
   
 
    app.conf.beat_schedule['send-weekly-email']['schedule'] = crontab(minute="*/15")

# def individual_gap(primary_key):
#     app.conf.beat_schedule['individual-periodic-task']['args'] = (primary_key,)
#     app.conf.beat_schedule['individual-periodic-task']['schedule'] = crontab(minute = "*/2")

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')



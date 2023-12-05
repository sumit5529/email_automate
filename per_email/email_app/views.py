from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from .models import Subscriber,EmailModel
from .forms import SubscriberForm
from django.contrib import messages
from .forms import EmailForm,EmailContentForm,EmailIndividualForm
from django.conf import settings
from django.core.mail import send_mail
from .task import send_weekly_email,revoke_old_tasks,individual_gap
from django.utils import timezone
from datetime import datetime, timedelta
from per_email.celery import set_gap

from django.db.models.functions import Extract


# Create your views here.
def list_subscriber(request):
    subscribers = Subscriber.objects.all()
    return render(request, 'email_app/list_subscriber.html', {'subscribers': subscribers})

def add_subscriber(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['name']
            useremail = form.cleaned_data['email']
            if Subscriber.objects.filter(name=username).count()==0 and Subscriber.objects.filter(email=useremail).count()==0:
                form.save()
                
            else:
                # messages.success(request, 'This user already exist ')
                form = SubscriberForm()
                return render(request, 'email_app/add_subscriber.html', {'form': form})
             
             
             
            return redirect('list_subscriber')  
    else:
        form = SubscriberForm()
    return render(request, 'email_app/add_subscriber.html', {'form': form})

def update_email(request):
    if(request.method=='POST'):
        form = EmailContentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_subscriber')
        
        else:

           form = EmailContentForm()
        return render(request, 'email_app/email_content.html', {'form': form})
    else:
        form = EmailContentForm()
    return render(request, 'email_app/email_content.html', {'form': form})


def send_email(request):
    # emailobj= EmailModel.objects.all().first()
    # subject = emailobj.subject
    # message_text = emailobj.message_text
   

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            emailobj= EmailModel.objects.all().first()
            
            subject = emailobj.subject
            message_text = emailobj.message_text
            schedule_date = form.cleaned_data['schedule_date']
            schedule_time = form.cleaned_data['schedule_time']
            periodic_gap_day = form.cleaned_data['periodic_gap_day']
            # inst = get_object_or_404(Subscriber)
            recipient_email = '20bec044@nith.ac.in'
            print('before sending')
            # rest_time = calculate_rest_time(schedule_date,schedule_time)
            # rest_time = int(rest_time)
            # print(rest_time)
            # revoke_old_tasks()
            # send_weekly_email.apply_async(args=[subject,message_text],countdown=rest_time)
            set_gap(periodic_gap_day)
            send_weekly_email()
            
            print('after sending')
          
            # message = message_text
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [recipient_email,]
            # send_mail( subject, message, email_from, recipient_list )
            
          

                

            return redirect('list_subscriber')
    else:
        form = EmailForm()

    return render(request, 'email_app/email_form.html', {'form': form})






def stop_mail(request):
    revoke_old_tasks()
    return redirect('list_subscriber')
    
# def separate_date_components(schedule_date):
    
#     # date_object = datetime.strptime(schedule_date, '%Y-%m-%d')
#     date_object = schedule_date

    
#     year = date_object.year
#     month = date_object.month
#     day = date_object.day

#     return year, month, day


# def separate_time_components(schedule_time):
   
#     time_object = schedule_time
    
#     hour = time_object.hour
#     minute = time_object.minute
#     second = 00
    
#     return hour,minute,second






# def calculate_rest_time(schedule_date,schedule_time):
   
    
#     year, month, day = separate_date_components(schedule_date)
#     hour,minute,second = separate_time_components(schedule_time)
    
#     target_datetime = datetime(year, month, day, hour, minute, second).replace(microsecond=0)


 
#     current_datetime = datetime.now().replace(microsecond=0)



#     time_difference = target_datetime - current_datetime

#     rest_time_seconds = max(time_difference.total_seconds(), 0)

#     return rest_time_seconds


def mail_individual(request,id):
    item = Subscriber.objects.get(id=id)
    print("done")
    form = EmailIndividualForm(request.POST or None,instance=item)
    context = {
        'item':item,
        'form':form,
    }
    if form.is_valid():
        form.save()
        return redirect('list_subscriber')
    return render (request,'email_app/email_individual.html',context)

def schedule_individual(request,id):
    if request.method=='POST':
        form = EmailForm(request.POST)
        if form.is_valid():
         
         schedule_date = form.cleaned_data['schedule_date']
         schedule_time = form.cleaned_data['schedule_time']
         gap = form.cleaned_data['periodic_gap_day']
         individual_gap(id,gap)
         return redirect('list_subscriber')
        
    else:
        form = EmailForm()

    return render(request, 'email_app/email_form.html', {'form': form})







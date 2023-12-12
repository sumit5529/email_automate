from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404
from .models import Subscriber,EmailHistory,EmailPlusScheduleModel

from django.contrib import messages
from .forms import SubscriberForm,EmailplusScheduleForm
from django.conf import settings


from django.utils import timezone
from datetime import datetime, timedelta


from django.db.models.functions import Extract
from rest_framework import viewsets
from .serializers import subscriber_serializer,email_plus_schedule_serializer,email_history_serializer
from rest_framework.decorators import action,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

""" apis """

class subscriber_viewset(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = subscriber_serializer
    # permission_classes = [IsAuthenticated]
    # """in action if detail is true it means id is required """
    @action(detail=True,methods=['get'])
    def schedule_email (self,request,pk=None):
        try:
         subscriber = Subscriber.objects.get(pk=pk)
         email = EmailPlusScheduleModel.objects.filter(subscriber=subscriber)
         email_serializer = email_plus_schedule_serializer(email,many = True, context = {'request':request})
         return Response(email_serializer.data)
        except Exception as e:
           return Response(
              {
                 'message':'This subsciber has no email scheduled'
              }
           )
        

    @action(detail=True,methods=['get'])
    def past_history(self,request,pk=None):
        try:
         subscriber = Subscriber.objects.get(pk=pk)
         email = EmailHistory.objects.filter(subscriber=subscriber)
         email_serializer = email_history_serializer(email,many = True, context = {'request':request})
         return Response(email_serializer.data)
        except Exception as e:
           return Response(
              {
                 'message':'No past History'
              }
           )
         



class email_plus_schedule_viewset(viewsets.ModelViewSet):
    queryset = EmailPlusScheduleModel.objects.all()
    serializer_class = email_plus_schedule_serializer

class email_history_viewset(viewsets.ModelViewSet):
    queryset = EmailHistory.objects.all()
    serializer_class = email_history_serializer


















""" subscriber information"""

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
                messages.success(request, 'This user already exist ')
                form = SubscriberForm()
                return render(request, 'email_app/add_subscriber.html', {'form': form})
             
             
             
            return redirect('email_app:list_subscriber')  
    else:
        messages.success(request, 'This user already exist ')
        form = SubscriberForm()
    return render(request, 'email_app/add_subscriber.html', {'form': form})


""" to change the name or email of subscriber having pk = id"""
def update_subscriber(request,id):
    subscriber = get_object_or_404(Subscriber, id=id)

    # Check if the request method is POST
    if request.method == 'POST':
      
        form = SubscriberForm(request.POST,instance=subscriber)
        if form.is_valid():
         email = form.cleaned_data['email']
         name = form.cleaned_data['name']

         subscriber.name = name
         subscriber.email = email
         subscriber.save()   
         detail_url = reverse('email_app:list_subscriber')
         return redirect (detail_url)
            # return redirect('list_subscriber')

    else:
        form = SubscriberForm(instance=subscriber)

    context = {
        'form': form,
        'subscriber': subscriber,
    }

    return render(request, 'email_app/add_subscriber.html', context)


def delete_subscriber(request,id):
    subscriber = get_object_or_404(Subscriber, id=id)
    if request.method == 'POST':
        subscriber.delete()
        return redirect('email_app:list_subscriber')
    else:
        return render (request,'email_app/delete_subscriber.html',{'subscriber':subscriber})












""" to diplay all past sent email with subject,message,timestamp etc"""
def email_history_for_subscriber(request, id):
    subscriber = Subscriber.objects.get(id=id)
    email_history_entries = EmailHistory.objects.filter(subscriber=subscriber).order_by('-timestamp')
    return render(request, 'email_app/email_history.html', {'subscriber': subscriber, 'email_history_entries': email_history_entries})

""" To display the all scheduled email content of user having pk = id"""
def Next_email_history(request,id):
    subscriber = Subscriber.objects.get(id=id)
    current_datetime = datetime.now()


    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
    email_history_list= EmailPlusScheduleModel.objects.filter(subscriber=subscriber,schedule_time__gt = formatted_datetime).order_by('schedule_time')
  
    return render(request, 'email_app/next_email_history.html', {'subscriber': subscriber, 'email_history_list': email_history_list})



""" for creating new email and scheduled that for user having pk = id"""
def EmailPlusSchedule(request,id):
   
    if(request.method=='POST'):
        form = EmailplusScheduleForm(request.POST)
        if form.is_valid():
            schedule_time = form.cleaned_data['schedule_time']
            gap = form.cleaned_data['gap']
            frequency = form.cleaned_data['frequency']
            message_text = form.cleaned_data['message_text']
            subject = form.cleaned_data['subject']
            subscriber = Subscriber.objects.get(id = id)
            obj = EmailPlusScheduleModel.objects.create(
            subscriber=subscriber,
            subject = subject,
            message_text = message_text,
            schedule_time = schedule_time,
            gap = gap,
            frequency = frequency
          )
            if obj :
                print('done')
            detail_url = reverse('email_app:email_plus_schedulelist', args=[id])
            return redirect (detail_url)
            
        
        else:
           print('form is not valid')
           form = EmailplusScheduleForm()
        return render(request, 'email_app/EmailPlusSchedule.html', {'form': form})
    else:
        form = EmailplusScheduleForm()
    return render(request, 'email_app/EmailPlusSchedule.html', {'form': form})


def delete_email(request,id):
    obj = EmailPlusScheduleModel.objects.get(id=id)
    detail_url = reverse('email_app:email_plus_schedulelist', args=[obj.subscriber.pk])
        
    obj.delete()
    return redirect (detail_url)




"""display to list of all scheduled email of subscriber having pk = id"""
def EmailPlusScheduleList(request,id):
    subscriber = Subscriber.objects.get(id=id)
    EmailList = EmailPlusScheduleModel.objects.filter(subscriber = subscriber)
    return render(request, 'email_app/list_EmailPlusSchedule.html', {'EmailList':EmailList,'subscriber':subscriber})

"""It is used to view the email content and sheduling time of email object having pk = id"""
def EmailPlusScheduleview(request,id):
    EmailPlusScheduleobj = get_object_or_404(EmailPlusScheduleModel, id=id)
    return render(request,'email_app/view_EmailPlusSchedule.html',{'EmailPlusScheduleobj':EmailPlusScheduleobj})


"""to change the email content or sheduling time of email object having pk = id"""
def EmailPlusScheduleChange(request, id):
    # Retrieve the existing object from the database
    EmailPlusSchedule = get_object_or_404(EmailPlusScheduleModel, id=id)

    # Check if the request method is POST
    if request.method == 'POST':
       
        form = EmailplusScheduleForm(request.POST, instance=EmailPlusSchedule)

       
        if form.is_valid():
            # Save the changes to the existing object
            form.save()
            
            detail_url = reverse('email_app:email_plus_schedulelist', args=[EmailPlusSchedule.subscriber.pk])
            return redirect (detail_url)
            

    else:
        # If the request method is not POST, create the form with the existing instance
        form = EmailplusScheduleForm(instance=EmailPlusSchedule)

    context = {
        'form': form,
        'EmailPlusSchedule': EmailPlusSchedule,
    }

    return render(request, 'email_app/EmailPlusSchedule.html', context)
























# def schedule_individual(request,id):
#     if request.method=='POST':
#         form = EmailForm(request.POST)
#         if form.is_valid():
         
#          schedule_date = form.cleaned_data['schedule_date']
#          schedule_time = form.cleaned_data['schedule_time']
#          gap = form.cleaned_data['periodic_gap_day']
#          subscriber = Subscriber.objects.get(id = id)
#          emailobj = NextEmailHistory.objects.filter(subscriber=subscriber).first()
#          if emailobj:
#              emailobj.schedule_date = schedule_date
#              emailobj.schedule_time =  schedule_time
#              emailobj.periodic_gap_day = gap
#              emailobj.save()
#          else:
#              NextEmailHistory.objects.create(subscriber=subscriber,schedule_date=schedule_date,
                                             
#                                         schedule_time=schedule_time,periodic_gap_day = gap)
         
             
#         individual_gap(id,gap)
#         return redirect('list_subscriber')
        
#     else:
#         form = EmailForm()

#     return render(request, 'email_app/email_form.html', {'form': form})



# def send_email(request):
   
   

#     if request.method == 'POST':
#         form = EmailForm(request.POST)
#         if form.is_valid():
#             emailobj= EmailModel.objects.all().first()
            
#             subject = emailobj.subject
#             message_text = emailobj.message_text
#             schedule_date = form.cleaned_data['schedule_date']
#             schedule_time = form.cleaned_data['schedule_time']
#             periodic_gap_day = form.cleaned_data['periodic_gap_day']
#             # inst = get_object_or_404(Subscriber)
#             recipient_email = '20bec044@nith.ac.in'
#             print('before sending')
#             # rest_time = calculate_rest_time(schedule_date,schedule_time)
#             # rest_time = int(rest_time)
#             # print(rest_time)
#             # revoke_old_tasks()
#             # send_weekly_email.apply_async(args=[subject,message_text],countdown=rest_time)
#             set_gap(periodic_gap_day)
#             send_weekly_email()
            
#             print('after sending')
          
#             # message = message_text
#             # email_from = settings.EMAIL_HOST_USER
#             # recipient_list = [recipient_email,]
#             # send_mail( subject, message, email_from, recipient_list )
            
          

                

#             return redirect('list_subscriber')
#     else:
#         form = EmailForm()

#     return render(request, 'email_app/email_form.html', {'form': form})






























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




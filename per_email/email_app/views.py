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
from .serializers import SubscriberSerializer,EmailPlusScheduleSerializer,EmailHistorySerializer
from rest_framework.decorators import action,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

""" apis """
"""Subscriber's api class using modelviewset which provide by default
get,put,post,delete etc action by default and url for these
is adjusted by router that is defined in urls.py
 ,"""
class subscriber_viewset(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    # permission_classes = [IsAuthenticated]

    """in action if detail is true it means id is required. It is for individual's
    detail like,provide api of list for individual schedule email and fun below of it 
    provide past history
     """
    @action(detail=True,methods=['get'])
    def schedule_email (self,request,pk=None):
        try:
         subscriber = Subscriber.objects.get(pk=pk)
         email = EmailPlusScheduleModel.objects.filter(subscriber=subscriber)
         email_serializer = EmailPlusScheduleSerializer(email,many = True, context = {'request':request})
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
         email_serializer = EmailHistorySerializer(email,many = True, context = {'request':request})
         return Response(email_serializer.data)
        except Exception as e:
           return Response(
              {
                 'message':'No past History'
              }
           )
         


"""This class is responsible for provinding api of Email and their scheduled time in json fromat"""
class email_plus_schedule_viewset(viewsets.ModelViewSet):
    queryset = EmailPlusScheduleModel.objects.all()
    serializer_class = EmailPlusScheduleSerializer

"""This class is responsible for provinding api of past email history in json fromat"""
class email_history_viewset(viewsets.ModelViewSet):
    queryset = EmailHistory.objects.all()
    serializer_class = EmailHistorySerializer


















""" subscriber information"""

""" This fun is responsible to display list of subscriber """
def list_subscriber(request):
    
   
    subscribers = Subscriber.objects.all()
    return render(request, 'email_app/list_subscriber.html', {'subscribers': subscribers})

""" Here new subscriber is added using form if with same email and username,any subsriber is already then 
it will not accept form and show that this user already exist and ask to fill form again """
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
            gp = form.cleaned_data['gp']
            frequency = form.cleaned_data['frequency']
            message_text = form.cleaned_data['message_text']
            subject = form.cleaned_data['subject']
            subscriber = Subscriber.objects.get(id = id)
            obj = EmailPlusScheduleModel.objects.create(
            subscriber=subscriber,
            subject = subject,
            message_text = message_text,
            schedule_time = schedule_time,
            gp = gp,
            frequency = frequency
          )
            # if obj :
            #     print('done')
            detail_url = reverse('email_app:email_plus_schedulelist', args=[id])
            return redirect (detail_url)
            
        
        else:
        #    print('form is not valid')
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





















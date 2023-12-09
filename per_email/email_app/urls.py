from django.urls import path
from . import views

app_name = 'email_app'

urlpatterns = [
    path('', views.list_subscriber, name='list_subscriber'),
    path('add/', views.add_subscriber, name='add_subscriber'),
    path('update_subscriber/<int:id>/',views.update_subscriber,name='update_subscriber'),
    path('delete_subscriber/<int:id>',views.delete_subscriber,name = 'delete_subscriber'),

   
   
   
    
    path('delete_email/<int:id>/',views.delete_email,name='delete_email'),
    path('email_history/<int:id>/',views.email_history_for_subscriber,name='email_history'),
    path('next_email_history/<int:id>/',views.Next_email_history,name='next_email_history'),
    path('EmailPlusScheduleList/<int:id>',views.EmailPlusScheduleList,name='email_plus_schedulelist'),
    path('EmailPlusScheduleList/<int:id>/create_new',views.EmailPlusSchedule,name='new_email'),
    path('change_EmailSchedule/<int:id>',views.EmailPlusScheduleChange,name='ChangeEmailSchedule'),
    path('view_EmailSchedule/<int:id>',views.EmailPlusScheduleview,name='viewEmailSchedule'),
   
    
    
]

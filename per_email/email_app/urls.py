from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_subscriber, name='list_subscriber'),
    path('add/', views.add_subscriber, name='add_subscriber'),
    # path('<int:pk>/', views.edit_customer, name='edit_customer'),
    # path('<int:pk>/delete/', views.delete_customer, name='delete_customer'),
    path('send_email/',views.send_email,name='send_email'),
    path('update_email/',views.update_email,name='update_email'),
    path('stop_email',views.stop_mail,name='stop_mail'),
    # path('mail_individual/<int:id>/',views.mail_individual,name='mail_individual'),
    path('schedule_individual/<int:id>/',views.schedule_individual,name='schedule_individual'),
    path('email_history/<int:id>/',views.email_history_for_subscriber,name='email_history'),
    path('next_email_history/<int:id>/',views.Next_email_history,name='next_email_history'),
    path('EmailPlusScheduleList/<int:id>',views.EmailPlusScheduleList,name='email_plus_schedulelist'),
    path('EmailPlusScheduleList/<int:id>/create_new',views.EmailPlusSchedule,name='new_email'),
    path('change_EmailSchedule/<int:id>',views.EmailPlusScheduleChange,name='ChangeEmailSchedule'),
    path('view_EmailSchedule/<int:id>',views.EmailPlusScheduleview,name='viewEmailSchedule'),
   
    
    
]

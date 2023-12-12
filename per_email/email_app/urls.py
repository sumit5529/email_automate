from django.urls import path,include
from . import views

from rest_framework import routers
from .views import subscriber_viewset,email_plus_schedule_viewset,email_history_viewset


app_name = 'email_app'
router = routers.DefaultRouter()
router.register(r'api_subscriber',subscriber_viewset,basename='api_subscriber')
router.register(r'schedule_email',email_plus_schedule_viewset,basename='schedule_email')
router.register(r'past_history',email_history_viewset,basename='past_history')





urlpatterns = [
    path('', views.list_subscriber, name='list_subscriber'),
    path('',include(router.urls)),
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

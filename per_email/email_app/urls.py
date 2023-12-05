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
    path('mail_individual/<int:id>/',views.mail_individual,name='mail_individual'),
    path('schedule_individual/<int:id>/',views.schedule_individual,name='schedule_individual'),
]

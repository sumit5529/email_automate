from django.contrib import admin

# Register your models here.

from .models import Subscriber,EmailHistory,EmailPlusScheduleModel

admin.site.register(Subscriber)

admin.site.register(EmailHistory)



@admin.register(EmailPlusScheduleModel)
class EmailPlusScheduleModel(admin.ModelAdmin):
    list_filter = ('frequency',)  # Add fields you want to filter on
    list_display = ('subscriber', 'subject', 'frequency')  # Add fields you want to display

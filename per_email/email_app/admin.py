from django.contrib import admin

# Register your models here.

from .models import Subscriber,EmailModel,EmailHistory,NextEmailHistory,EmailPlusScheduleModel

admin.site.register(Subscriber)
admin.site.register(EmailModel)
admin.site.register(EmailHistory)
admin.site.register(NextEmailHistory)
# admin.site.register(EmailPlusScheduleModel)



@admin.register(EmailPlusScheduleModel)
class EmailPlusScheduleModel(admin.ModelAdmin):
    list_filter = ('frequency',)  # Add fields you want to filter on
    list_display = ('subscriber', 'subject', 'frequency')  # Add fields you want to display

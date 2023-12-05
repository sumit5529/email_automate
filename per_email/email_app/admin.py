from django.contrib import admin

# Register your models here.

from .models import Subscriber,EmailModel,EmailHistory,NextEmailHistory

admin.site.register(Subscriber)
admin.site.register(EmailModel)
admin.site.register(EmailHistory)
admin.site.register(NextEmailHistory)
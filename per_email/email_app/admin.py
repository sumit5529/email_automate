from django.contrib import admin

# Register your models here.

from .models import Subscriber,EmailModel

admin.site.register(Subscriber)
admin.site.register(EmailModel)
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([User, Chat, Location, Company, Job, Message, Notification])

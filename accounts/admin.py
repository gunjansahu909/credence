from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Developer)
admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(Work_Status)
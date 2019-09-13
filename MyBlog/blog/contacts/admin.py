from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']

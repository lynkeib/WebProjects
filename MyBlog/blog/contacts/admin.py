from django.contrib import admin
from .models import Contacts


# Register your models here.
# @admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message', 'created_time')


admin.site.register(Contacts, ContactsAdmin)

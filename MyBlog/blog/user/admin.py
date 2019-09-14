from django.contrib import admin
from .models import User, ConfirmString


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email', 'has_confirmed')


class ConfirmStringAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'c_time')


admin.site.register(User, UserAdmin)
admin.site.register(ConfirmString, ConfirmStringAdmin)

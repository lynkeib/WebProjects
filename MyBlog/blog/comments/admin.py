from django.contrib import admin
from .models import Comments


# Register your models here.


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'url', 'text', 'created_time', 'article', 'username')


admin.site.register(Comments, CommentsAdmin)

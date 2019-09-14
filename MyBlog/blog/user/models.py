from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.TextField()
    created_time = models.TimeField(auto_now_add=True)


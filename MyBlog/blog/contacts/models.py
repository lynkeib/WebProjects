from django.db import models


# Create your models here.
class Contacts(models.Model):
    def __str__(self):
        return self.subject

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField(blank=True)
    created_time = models.TimeField(auto_now_add=True, blank=True, null=True)

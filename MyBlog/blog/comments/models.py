from django.db import models


# Create your models here.

class Comments(models.Model):
    def __str__(self):
        return self.text[:20]

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=225)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.TimeField(auto_now_add=True)
    article = models.ForeignKey('home.Article', on_delete=models.CASCADE, null=True, blank=True)
    username = models.TextField(default="NONE")

from django.db import models


# Create your models here.
class Article(models.Model):
    ArticleId = models.AutoField(primary_key=True)
    Title = models.TextField()
    BriefContent = models.TextField()
    Content = models.TextField()
    PublishDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Title

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import markdown
from django.utils.html import strip_tags


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Article(models.Model):
    def __str__(self):
        return self.title

    # Title
    title = models.CharField(max_length=70)

    # Content
    body = models.TextField()

    # Time
    created_time = models.DateTimeField(null=True)
    modified_time = models.DateTimeField(null=True)

    # Abstract
    excerpt = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:500]
        super(Article, self).save(*args, **kwargs)

    # Tags
    category = models.ForeignKey(Category, on_delete="SET_NULL", null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    # Auth
    author = models.ForeignKey(User, on_delete="SET_NULL")

    # Views
    views = models.PositiveIntegerField(default=0)

    # GetURL
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    # Increase Views
    def increase_view(self):
        self.views += 1
        self.save(update_fields=['views'])

    # Ordering
    class Meta:
        ordering = ['-created_time']

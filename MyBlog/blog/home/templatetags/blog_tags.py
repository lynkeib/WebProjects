from ..models import Article
from ..models import Category
from ..models import Tag
from django import template
from django.db.models.aggregates import Count

register = template.Library()


@register.simple_tag
def get_rencent_articles(num=5):
    return Article.objects.all()[:num]


@register.simple_tag
def archives():
    return Article.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_article=Count('article')).filter(num_article__gt=0)


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_article=Count('article')).filter(num_article__gt=0)

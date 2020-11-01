from typing import Dict

from django.db.models import DateTimeField, AutoField, TextField
from django.http import HttpResponse, JsonResponse, HttpRequest

# Create your views here.
from blog.ArticleManager import ArticleManager
from blog.models import Article


def hello_world(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello World")


def article_content(request: HttpRequest) -> HttpResponse:
    this_article: Article = ArticleManager.get_all()[0]
    data: Dict = wrap_article_response(this_article)
    return HttpResponse(data)


def wrap_article_response(article: Article) -> Dict:
    title: TextField = article.Title
    brief_content: TextField = article.BriefContent
    content: TextField = article.Content
    article_id: AutoField = article.ArticleId
    publish_date: DateTimeField = article.PublishDate
    data: Dict = {
        title: title,
        brief_content: brief_content,
        content: content,
        article_id: article_id,
        publish_date: publish_date
    }
    return data

from typing import Dict, List

from django.db.models import DateTimeField, AutoField, TextField
from django.http import HttpResponse, JsonResponse, HttpRequest

# Create your views here.
from django.shortcuts import render

from blog.ArticleManager import ArticleManager
from blog.models import Article


def get_index_page(request: HttpRequest) -> HttpResponse:
    articles: List[Article] = ArticleManager.get_all()
    return render(request, "blog/index.html", {"articles": articles})


def get_detail_page(request: HttpRequest, article_id: int) -> HttpResponse:
    article: Article = ArticleManager.get_by_id(article_id)
    return render(request, "blog/detail.html", {"article": article})


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

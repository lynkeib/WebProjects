from django.conf.urls import url

from . import views

app_name = 'comments'
urlpatterns = [
    url(r'^comment/article/(?P<article_pk>\d*)/$', views.post, name='comments'),
]
"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from home import views as home_view
from comments import views as comments_view
from django.conf.urls.static import static
from . import settings
from home.feeds import AllPostsRssFeed


# from django.conf.urls import url

urlpatterns = [
                  path('admin/', admin.site.urls),
                  re_path(r'^index.*?', home_view.HomeView.as_view(), name='index'),
                  re_path(r'^$', home_view.homepage, name='home'),
                  re_path(r"^homepage/$", home_view.homepage, name='homepage'),
                  re_path(r'^articles.html$', home_view.ArticlesView.as_view(), name="articles"),
                  re_path(r'^articles/(?P<pk>\d+)/$', home_view.ArticleDetailsView.as_view(), name='detail'),
                  re_path(r"^about.*?$", home_view.about, name='about'),
                  re_path(r"", include('contacts.urls')),
                  re_path(r"^archives/(?P<year>\d{4})/(?P<month>\d{1,2})/$", home_view.archives, name='archives'),
                  re_path(r"^category/(?P<pk>\d+)/$", home_view.CategoryView.as_view(), name='categories'),
                  re_path(r"^tag/(?P<pk>\d+)/$", home_view.TagView.as_view(), name='tag'),
                  re_path(r"", include('comments.urls')),
                  re_path(r"^all/rss/$", AllPostsRssFeed(), name='rss'),
                  # re_path(r"^search/$", home_view.search, name='search')
                  re_path(r"^search/", include('haystack.urls')),
                  re_path(r"", include('user.urls'))
              ] + static(settings.STATIC_URL)

from django.contrib.syndication.views import Feed

from .models import Article


class AllPostsRssFeed(Feed):
    title = "BLOG from Connor~"

    link = "/"

    description = "this is my blog"

    def items(self):
        return Article.objects.all()

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.body

from django.contrib import admin
from .models import Category
from .models import Tag
from .models import Article


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    # fields = ['name']
    list_display = ('name',)


class TagAdmin(admin.ModelAdmin):
    # fields = ['name']
    list_display = ('name',)

    # def get_tags(self, obj):
    #     return ','.join([tag.name for tag in obj.tags.all()])


class ArticleAdmin(admin.ModelAdmin):
    # fields = ['title', 'body', 'created_time', 'modified_time', 'excerpt', 'category', 'tags', 'author']
    list_display = (
        'title', 'created_time', 'modified_time', 'excerpt', 'category', 'get_tags', 'author', 'views')

    def get_tags(self, obj):
        return ','.join([tag.name for tag in obj.tags.all()])


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)

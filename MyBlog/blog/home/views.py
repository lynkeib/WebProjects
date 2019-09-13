from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Article, Category, Tag
import markdown
from comments.form import CommentForm
from django.views.generic import ListView, DetailView
from django.db.models import Q


# Create your views here.
# def home(request):
#     a_list = Article.objects.all()
#     if request.method == "POST":
#         return
#     return render(request, 'index.html', context={'a_list': a_list})

# Try ListView

def homepage(request):
    return render(request, "homepage.html")


class HomeView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'a_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False

        first = False

        last = False

        page_number = page.number

        total_pages = paginator.num_pages

        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


## Try ListView
# def categories(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     article_list = Article.objects.filter(category=cate)
#     return render(request, 'index.html', {'a_list': article_list})
class CategoryView(HomeView):
    # model = Article
    # template_name = 'index.html'
    # context_object_name = 'a_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(HomeView):

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tag)


def archives(request, year, month):
    article_list = Article.objects.filter(created_time__year=year,
                                          created_time__month=month)
    return render(request, 'index.html', {'a_list': article_list})


class ArchiveView(ListView):
    def get_queryset(self):
        return super().get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                             created_time__month=self.kwargs.get('month'))


## super(Class, self).xx == super().xxx

def index(request):
    return HttpResponseRedirect('/')


def articles(request):
    return render(request, 'index.html')


class ArticlesView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'a_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False

        first = False

        last = False

        page_number = page.number

        total_pages = paginator.num_pages

        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


def about(request):
    return render(request, "about.html")


def contact(request):
    # if request == "POST":
    #     form = CommentForm

    return render(request, "contact.html")


# def single(request, pk):
#     article = get_object_or_404(Article, pk=pk)
#     article.increase_view()
#     article.body = markdown.markdown(article.body,
#                                      extensions=[
#                                          'markdown.extensions.extra',
#                                          'markdown.extensions.codehilite',
#                                          'markdown.extensions.toc',
#                                      ])
#     form = CommentForm()
#     comment_list = article.comments_set.all()
#     context = {'article': article,
#                'form': form,
#                'comment_list': comment_list}
#     return render(request, "detail.html", context=context)
class ArticleDetailsView(DetailView):
    model = Article
    template_name = 'detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_view()
        return response

    def get_object(self, queryset=None):
        article = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ])
        article.body = md.convert(article.body)
        article.toc = md.toc
        return article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comments_set.all()
        context.update({'form': form, 'comment_list': comment_list})
        return context


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "Please type in some words"
        return render(request, 'index.html', {'error_msg': error_msg})

    a_list = Article.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'index.html', {'error_msg': error_msg,
                                          'a_list': a_list})


def homepage(request):
    return render(request, 'homepage.html')

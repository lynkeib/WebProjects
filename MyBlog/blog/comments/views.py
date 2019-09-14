from django.shortcuts import render, get_object_or_404, redirect
from home.models import Article
from .models import Comments
from .form import CommentForm


# Create your views here.
def post(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.username = request.session.get("user_name")
            comment.save()
            return redirect(article)
        else:
            comment_list = article.comments_set.all()
            context = {'article': article,
                       'form': form,
                       'comment_list': comment_list}
            return render(request, 'detail.html', context=context)
    return redirect(article)

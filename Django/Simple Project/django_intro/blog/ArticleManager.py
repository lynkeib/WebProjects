from typing import List

from .models import Article


class ArticleManager:

    @classmethod
    def get_all(cls) -> List[Article]:
        return Article.objects.all()

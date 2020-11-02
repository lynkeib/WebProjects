from typing import List

from .models import Article
import logging
from django_intro import settings

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)


class ArticleManager:

    @classmethod
    def get_all(cls) -> List[Article]:
        logger.info("Getting all articles")
        return Article.objects.all()

from typing import List

from hub_blog.models import Article, Comment, Rating


class ArticleRepository:
    def add_article(self, article: Article) -> Article:
        raise NotImplementedError()

    def get_article_by_id(self, article_id: str) -> Article:
        raise NotImplementedError()

    def list_articles_by_tags(self, tags: List[str]) -> List[Article]:
        raise NotImplementedError()

    def list_articles_by_keywords(self, keywords: List[str]) -> List[Article]:
        raise NotImplementedError()

    def rate_article(self, rating: Rating) -> Article:
        raise NotImplementedError()

    def delete_article(self, article_id: str) -> None:
        raise NotImplementedError()

    def add_comment(self, comment: Comment) -> Comment:
        raise NotImplementedError()

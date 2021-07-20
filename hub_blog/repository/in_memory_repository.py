from typing import List, Mapping

from hub_blog.exceptions import ArticleNotFoundException
from hub_blog.models import Article, Comment, Rating
from hub_blog.repository.repository import ArticleRepository


class InMemoryArticleRepository(ArticleRepository):
    def __init__(self) -> None:
        self.articles: Mapping[str, Article] = {}
        self.articles_by_tags: Mapping[str, List[str]] = {}
        self.articles_by_keywords: Mapping[str, List[str]] = {}
        self.comments: Mapping[str, List[str]] = {}

    def add_article(self, article: Article) -> Article:
        self.articles[article.article_id] = article

        for tag in article.tags:
            self.articles_by_tags.setdefault(tag, []).append(article.article_id)

        # TODO: improve keywords by using tokenization/stemming/
        # stopwords removal and use article content to extract keywords
        for keyword in article.title.split(' '):
            self.articles_by_keywords.setdefault(keyword, []).append(article.article_id)

    def get_article_by_id(self, article_id: str) -> Article:
        if article_id not in self.articles:
            raise ArticleNotFoundException(article_id=article_id)
        return self.articles[article_id]

    def list_articles_by_tags(self, tags: List[str]) -> List[Article]:
        article_ids = []
        for tag in tags:
            if tag in self.articles_by_tags:
                article_ids.extend(self.articles_by_tags[tag])

        return list(set([
            self.articles[article_id] for article_id in set(article_ids)
            if article_id in self.articles
        ]))

    def list_articles_by_keywords(self, keywords: List[str]) -> List[Article]:
        article_ids = []
        for keyword in keywords:
            if keyword in self.articles_by_keywords:
                article_ids.extend(self.articles_by_keywords[keyword])

        return list(set([
            self.articles[article_id] for article_id in set(article_ids)
            if article_id in self.articles
        ]))

    def rate_article(self, rating: Rating) -> Article:
        if rating.article_id not in self.articles:
            raise ArticleNotFoundException(article_id=rating.article_id)

        if rating.upvote:
            self.articles[rating.article_id].upvotes += 1
        else:
            self.articles[rating.article_id].downvotes += 1

        return self.articles[rating.article_id]

    def delete_article(self, article_id: str) -> None:
        if article_id not in self.articles:
            raise ArticleNotFoundException(article_id=article_id)

        tags = self.articles[article_id].tags
        for tag in tags:
            self.articles_by_tags[tag].remove(article_id)
            if not self.articles_by_tags[tag]:
                del self.articles_by_tags[tag]

        keywords = self.articles[article_id].title.split(' ')
        for keyword in keywords:
            self.articles_by_keywords[keyword].remove(article_id)
            if not self.articles_by_keywords[keyword]:
                del self.articles_by_keywords[keyword]

        del self.articles[article_id]

    def add_comment(self, comment: Comment) -> Comment:
        if comment.article_id not in self.articles:
            raise ArticleNotFoundException(article_id=comment.article_id)

        self.comments = comment
        self.articles[comment.article_id].comment_ids.append(comment.comment_id)

        return comment

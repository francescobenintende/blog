import pytest

from hub_blog.exceptions import ArticleNotFoundException
from hub_blog.models import Article, Comment, Rating
from hub_blog.repository.in_memory_repository import InMemoryArticleRepository

test_article = Article(
    article_id='uuid-generated',
    title='Titles make keywords',
    content='Lots of content.',
    tags=['tag1', 'tag2'],
    user_id='user_id',
    upvotes=3,
    downvotes=2,
    comment_ids=[],
)


class TestAddArticle:
    def test_add_article_adds_article_to_articles_and_articles_by_tags_and_articles_by_keywords(self):
        repo = InMemoryArticleRepository()
        repo.add_article(article=test_article)

        assert len(repo.articles) == 1
        assert repo.articles[test_article.article_id] == test_article

        assert len(repo.articles_by_tags) == 2
        assert repo.articles_by_tags[test_article.tags[0]] == [test_article.article_id]
        assert repo.articles_by_tags[test_article.tags[1]] == [test_article.article_id]

        assert len(repo.articles_by_keywords) == 3
        assert repo.articles_by_keywords['Titles'] == [test_article.article_id]
        assert repo.articles_by_keywords['make'] == [test_article.article_id]
        assert repo.articles_by_keywords['keywords'] == [test_article.article_id]


class TestGetArticleById:
    def test_get_article_by_id_returns_article(self):
        repo = InMemoryArticleRepository()
        repo.articles[test_article.article_id] = test_article
        repo.articles_by_tags[test_article.tags[0]] = [test_article.article_id]
        repo.articles_by_tags[test_article.tags[1]] = [test_article.article_id]
        repo.articles_by_keywords['Titles'] = [test_article.article_id]
        repo.articles_by_keywords['make'] = [test_article.article_id]
        repo.articles_by_keywords['keywords'] = [test_article.article_id]

        returned_article = repo.get_article_by_id(article_id=test_article.article_id)

        assert test_article == returned_article

    def test_get_article_by_id_raises_exception_when_article_id_not_found(self):
        repo = InMemoryArticleRepository()

        with pytest.raises(ArticleNotFoundException):
            repo.get_article_by_id(article_id='a non-existent article id')


class TestListArticlesByTags:
    def test_list_articles_by_tags_returns_articles_corresponding_to_tags(self):
        repo = InMemoryArticleRepository()
        article_two = Article(
            article_id='uuid-generated-two',
            title='Experiences make people',
            content='Lots of content.',
            tags=['tag3', 'tag4'],
            user_id='user_id_2',
            upvotes=3,
            downvotes=2,
            comment_ids=['comment-id-2'],
        )

        repo.articles[test_article.article_id] = test_article
        repo.articles_by_tags[test_article.tags[0]] = [test_article.article_id]
        repo.articles_by_tags[test_article.tags[1]] = [test_article.article_id]

        repo.articles[article_two.article_id] = article_two
        repo.articles_by_tags[article_two.tags[0]] = [article_two.article_id]
        repo.articles_by_tags[article_two.tags[1]] = [article_two.article_id]

        print(repo)
        returned_articles = repo.list_articles_by_tags(['tag2', 'tag4'])

        assert len(returned_articles) == 2
        assert test_article in returned_articles
        assert article_two in returned_articles

    def test_list_articles_by_tags_returns_empty_list_when_no_matching_tags_are_present(self):
        repo = InMemoryArticleRepository()
        returned_articles = repo.list_articles_by_tags(['tag1'])

        assert len(returned_articles) == 0


class TestListArticlesByKeywords:
    def test_list_articles_by_keywords_returns_articles_corresponding_to_tags(self):
        repo = InMemoryArticleRepository()
        article_two = Article(
            article_id='uuid-generated-two',
            title='Keywords',
            content='Lots of content.',
            tags=['tag3', 'tag4'],
            user_id='user_id_2',
            upvotes=3,
            downvotes=2,
            comment_ids=['comment-id-2'],
        )

        repo.articles[test_article.article_id] = test_article
        repo.articles_by_keywords['Titles'] = [test_article.article_id]

        repo.articles[article_two.article_id] = article_two
        repo.articles_by_keywords['Keywords'] = [article_two.article_id]

        returned_articles = repo.list_articles_by_keywords(['Titles', 'Keywords'])

        assert len(returned_articles) == 2
        assert test_article in returned_articles
        assert article_two in returned_articles

    def test_list_articles_by_keywords_returns_empty_list_when_no_matching_tags_are_present(self):
        repo = InMemoryArticleRepository()
        returned_articles = repo.list_articles_by_keywords(['non-existing-keyword'])

        assert len(returned_articles) == 0


class TestRateArticle:
    def test_rate_article_with_upvote_true_increments_upvotes(self):
        repo = InMemoryArticleRepository()
        repo.articles[test_article.article_id] = test_article

        rating = Rating(
            rating_id='uuid-generated',
            user_id='user_id',
            article_id=test_article.article_id,
            upvote=True
        )

        returned_article = repo.rate_article(rating=rating)

        assert 4 == returned_article.upvotes
        assert test_article.downvotes == returned_article.downvotes

    def test_rate_article_with_upvote_false_increments_downvotes(self):
        repo = InMemoryArticleRepository()
        repo.articles[test_article.article_id] = test_article

        rating = Rating(
            rating_id='uuid-generated',
            user_id='user_id',
            article_id=test_article.article_id,
            upvote=False
        )

        returned_article = repo.rate_article(rating=rating)

        assert 3 == returned_article.downvotes
        assert test_article.upvotes == returned_article.upvotes

    def test_rate_article_raises_article_not_found_exception_when_article_does_not_exist(self):
        repo = InMemoryArticleRepository()

        rating = Rating(
            rating_id='uuid-generated',
            user_id='user_id',
            article_id='non-existent-id',
            upvote=False
        )
        
        with pytest.raises(ArticleNotFoundException):
            repo.rate_article(rating=rating)


class TestDeleteArticle:
    def test_delete_article_deletes_article_from_articles_and_articles_by_tag_and_articles_by_keyword(self):
        repo = InMemoryArticleRepository()
        repo.articles[test_article.article_id] = test_article
        repo.articles_by_tags[test_article.tags[0]] = [test_article.article_id]
        repo.articles_by_tags[test_article.tags[1]] = [test_article.article_id]
        repo.articles_by_keywords['Titles'] = [test_article.article_id]
        repo.articles_by_keywords['make'] = [test_article.article_id]
        repo.articles_by_keywords['keywords'] = [test_article.article_id]

        repo.delete_article(article_id=test_article.article_id)

        assert len(repo.articles) == 0
        assert len(repo.articles_by_tags) == 0
        assert len(repo.articles_by_keywords) == 0

    def test_delete_article_raises_article_not_found_exception_when_article_does_not_exist(self):
        repo = InMemoryArticleRepository()

        with pytest.raises(ArticleNotFoundException):
            repo.delete_article(article_id='a non-existent article id')


class TestAddComment:
    def test_add_comment_add_comment_to_comments_and_comment_id_to_article(self):
        repo = InMemoryArticleRepository()
        repo.articles[test_article.article_id] = test_article

        comment = Comment(
            comment_id='some-generated-uuid',
            article_id=test_article.article_id,
            user_id='user_id',
            content='LGTM',
        )
        repo.add_comment(comment=comment)

        assert [comment.comment_id] == repo.articles[test_article.article_id].comment_ids

    def test_add_comment_raises_article_not_found_exception_when_article_does_not_exist(self):
        repo = InMemoryArticleRepository()

        with pytest.raises(ArticleNotFoundException):
            comment = Comment(
                comment_id='some-generated-uuid',
                article_id='non-existing-id',
                user_id='user_id',
                content='LGTM',
            )
            repo.add_comment(comment=comment)

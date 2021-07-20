from flask import Flask, request

from hub_blog.exceptions import ArticleMissingTitleException, ArticleMissingContentException, \
    ArticleMissingUserIdException, ArticleNotFoundException, ArticleIncludingRatingException, \
    ArticleIncludingCommentsException, RatingMissingUserIdException, \
    RatingMissingUpvoteException, CommentMissingArticleIdException, CommentMissingUserIdException, \
    CommentMissingContentException, MultiFilteringException
from hub_blog.models import Article, Rating, Comment
from hub_blog.repository.in_memory_repository import InMemoryArticleRepository

app = Flask(__name__)

# if os.env('MYSQL'):
# repository = ...
repository = InMemoryArticleRepository()


@app.route("/articles", methods=["POST"])
def create_article():
    try:
        article = Article.from_json(request.json)
        repository.add_article(article=article)
        return article.to_json(), 201
    except (
            ArticleMissingTitleException,
            ArticleMissingContentException,
            ArticleMissingUserIdException,
            ArticleIncludingRatingException,
            ArticleIncludingCommentsException,
    ) as e:
        return {'error': e.message}, 422


@app.route("/articles/<article_id>", methods=["GET"])
def get_article(article_id):
    try:
        article = repository.get_article_by_id(article_id=article_id)
        return article.to_json(), 200
    except ArticleNotFoundException as e:
        return {'error': e.message}, 400


@app.route("/articles/<article_id>", methods=["DELETE"])
def delete_article(article_id):
    try:
        repository.delete_article(article_id=article_id)
        return {}, 200
    except ArticleNotFoundException as e:
        return {'error': e.message}, 400


@app.route("/articles/<article_id>", methods=["PUT"])
def rate_article(article_id):
    try:
        rating = Rating.from_json(request.json)
        article = repository.rate_article(rating=rating)
        return article.to_json(), 200
    except (
            ArticleNotFoundException,
            RatingMissingUserIdException,
            RatingMissingUpvoteException,
    ) as e:
        return {'error': e.message}, 400


@app.route("/articles/<article_id>", methods=["POST"])
def add_comment(article_id):
    try:
        comment = Comment.from_json(request.json)
        returned_comment = repository.add_comment(comment=comment)
        return returned_comment.to_json(), 200
    except (
            ArticleNotFoundException,
            CommentMissingArticleIdException,
            CommentMissingUserIdException,
            CommentMissingContentException,
    ) as e:
        return {'error': e.message}, 400


@app.route("/articles", methods=["GET"])
def list_articles():
    try:
        articles = []
        if 'tags' in request.json and 'keywords' in request.json:
            raise MultiFilteringException()
        elif 'tags' in request.json:
            articles.extend(repository.list_articles_by_tags(request.json['tags']))
        else:
            articles.extend(repository.list_articles_by_keywords(request.json['keywords']))

        return {article.article_id: article.to_json() for article in articles}, 200
    except MultiFilteringException as e:
        return {'error': e.message}, 400

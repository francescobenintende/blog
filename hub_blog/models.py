from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import List, Mapping

from hub_blog.exceptions import ArticleMissingTitleException, ArticleMissingContentException, \
    ArticleMissingUserIdException, ArticleIncludingRatingException, ArticleIncludingCommentsException, \
    CommentMissingUserIdException, CommentMissingContentException, \
    RatingMissingUserIdException, RatingMissingUpvoteException


@dataclass
class Article:
    article_id: str
    title: str
    content: str
    tags: List[str]
    user_id: str
    upvotes: int
    downvotes: int
    comment_ids: List[str]

    @staticmethod
    def from_json(request: Mapping) -> Article:
        if 'title' not in request:
            raise ArticleMissingTitleException()
        if 'content' not in request:
            raise ArticleMissingContentException()
        if 'user_id' not in request:
            raise ArticleMissingUserIdException()
        if 'upvotes' in request:
            raise ArticleIncludingRatingException()
        if 'downvotes' in request:
            raise ArticleIncludingRatingException()
        if 'comment_ids' in request:
            raise ArticleIncludingCommentsException()

        return Article(
            article_id=str(uuid.uuid4()),
            title=request['title'],
            content=request['content'],
            tags=request['tags'],
            user_id=request['user_id'],
            upvotes=0,
            downvotes=0,
            comment_ids=[],
        )

    def to_json(self) -> Mapping:
        return {
            'article_id': self.article_id,
            'title': self.title,
            'content': self.content,
            'tags': self.tags,
            'user_id': self.user_id,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'comment_ids': self.comment_ids,
        }

    def __hash__(self):
        return hash(self.__repr__())


@dataclass
class Comment:
    comment_id: str
    article_id: str
    user_id: str
    content: str

    @staticmethod
    def from_json(request: Mapping) -> Comment:
        if 'user_id' not in request:
            raise CommentMissingUserIdException()
        if 'content' not in request:
            raise CommentMissingContentException()

        return Comment(
            comment_id=str(uuid.uuid4()),
            article_id=request['article_id'],
            user_id=request['user_id'],
            content=request['content'],
        )

    def to_json(self) -> Mapping:
        return {
            'comment_id': self.comment_id,
            'article_id': self.article_id,
            'user_id': self.user_id,
            'content': self.content,
        }

    def __hash__(self):
        return hash(self.__repr__())


@dataclass
class Rating:
    rating_id: str
    user_id: str
    article_id: str
    upvote: bool

    @staticmethod
    def from_json(request: Mapping) -> Rating:
        if 'user_id' not in request:
            raise RatingMissingUserIdException()
        if 'upvote' not in request:
            raise RatingMissingUpvoteException()

        return Rating(
            rating_id=str(uuid.uuid4()),
            user_id=request['user_id'],
            article_id=request['article_id'],
            upvote=request['upvote'],
        )

class ArticleMissingTitleException(Exception):
    message = 'Missing article title'


class ArticleMissingContentException(Exception):
    message = 'Missing article content'


class ArticleMissingUserIdException(Exception):
    message = 'Missing article user id'


class ArticleIncludingRatingException(Exception):
    message = 'Cannot provide rating when creating article'


class ArticleIncludingCommentsException(Exception):
    message = 'Cannot provide comment ids when creating article'


class ArticleNotFoundException(Exception):
    def __init__(self, article_id: str):
        self.message = f'Could not find article with id: {article_id}'


class CommentMissingArticleIdException(Exception):
    message = 'Missing comment article id'


class CommentMissingUserIdException(Exception):
    message = 'Missing comment user id'


class CommentMissingContentException(Exception):
    message = 'Missing comment content'


class RatingMissingUserIdException(Exception):
    message = 'Missing rating user id'


class RatingMissingUpvoteException(Exception):
    message = 'Missing rating upvote'


class MultiFilteringException(Exception):
    message = 'Can only filter by tags OR keywords'

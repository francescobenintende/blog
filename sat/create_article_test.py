from hub_blog import app


class TestCreateArticle:
    def test_create_article_with_all_allowed_fields_creates_article(self):
        with app.test_client() as c:
            article_to_create = {
                'title': 'Article Title',
                'content': 'Lots of interesting content.',
                'tags': ['tech', 'finance'],
                'user_id': 'fran',
            }
            response = c.post('/articles', json=article_to_create)
            response = c.post('/articles', json=article_to_create)

            assert response.status_code == 201
            assert response.json['article_id'] is not None
            assert response.json['title'] == article_to_create['title']
            assert response.json['content'] == article_to_create['content']
            assert response.json['tags'] == article_to_create['tags']
            assert response.json['user_id'] == article_to_create['user_id']
            assert response.json['upvotes'] == 0
            assert response.json['comment_ids'] == []

    def test_create_article_without_title_returns_missing_title_error(self):
        with app.test_client() as c:
            article_to_create = {
                'content': 'Lots of interesting content.',
                'tags': ['tech', 'finance'],
                'user_id': 'fran',
            }
            response = c.post('/articles', json=article_to_create)

            assert response.status_code == 422
            assert response.json['error'] == 'Missing article title'

    def test_create_article_without_content_returns_missing_content_error(self):
        with app.test_client() as c:
            article_to_create = {
                'title': 'Article Title',
                'tags': ['tech', 'finance'],
                'user_id': 'fran',
            }
            response = c.post('/articles', json=article_to_create)

            assert response.status_code == 422
            assert response.json['error'] == 'Missing article content'

    def test_create_article_without_user_id_returns_missing_user_id_error(self):
        with app.test_client() as c:
            article_to_create = {
                'title': 'Article Title',
                'content': 'Lots of interesting content.',
                'tags': ['tech', 'finance'],
            }
            response = c.post('/articles', json=article_to_create)

            assert response.status_code == 422
            assert response.json['error'] == 'Missing article user id'

    def test_create_article_with_upvotes_returns_including_rating_error(self):
        with app.test_client() as c:
            article_to_create = {
                'title': 'Article Title',
                'content': 'Lots of interesting content.',
                'tags': ['tech', 'finance'],
                'user_id': 'fran',
                'upvotes': 100,
            }
            response = c.post('/articles', json=article_to_create)

            assert response.status_code == 422
            assert response.json['error'] == 'Cannot provide rating when creating article'

    def test_create_article_with_downvotes_returns_including_rating_error(self):
        with app.test_client() as c:
            article_to_create = {
                'title': 'Article Title',
                'content': 'Lots of interesting content.',
                'tags': ['tech', 'finance'],
                'user_id': 'fran',
                'downvotes': 200,
            }
            response = c.post('/articles', json=article_to_create)

            assert response.status_code == 422
            assert response.json['error'] == 'Cannot provide rating when creating article'

    def test_create_article_with_comment_ids_returns_including_comment_ids_error(self):
        with app.test_client() as c:
            article_to_create = {
                'title': 'Article Title',
                'content': 'Lots of interesting content.',
                'tags': ['tech', 'finance'],
                'user_id': 'fran',
                'comment_ids': ['some-comment-ids!', 'some-other-comment-ids']
            }
            response = c.post('/articles', json=article_to_create)

            assert response.status_code == 422
            assert response.json['error'] == 'Cannot provide comment ids when creating article'

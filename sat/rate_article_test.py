from hub_blog import app


class TestRateArticle:
    def test_rate_article_returns_article_with_updated_rating(self):
        with app.test_client() as c:
            article_to_create = {
                'title': 'Article Title',
                'content': 'Lots of interesting content.',
                'tags': ['tech', 'finance'],
                'user_id': 'fran',
            }
            create_response = c.post('/articles', json=article_to_create)
            assert create_response.status_code == 201

            article_id = create_response.json['article_id']
            rating = {
                'user_id': 'user_id',
                'article_id': article_id,
                'upvote': True,
            }

            rate_response = c.put(f'/articles/{article_id}', json=rating)
            assert rate_response.status_code == 200

            get_response = c.get(f'/articles/{article_id}')

            assert get_response.status_code == 200
            assert get_response.json['article_id'] is not None
            assert get_response.json['title'] == article_to_create['title']
            assert get_response.json['content'] == article_to_create['content']
            assert get_response.json['tags'] == article_to_create['tags']
            assert get_response.json['user_id'] == article_to_create['user_id']
            assert get_response.json['upvotes'] == 1
            assert get_response.json['comment_ids'] == []

    def test_rate_article_returns_article_not_found_error_when_article_id_does_not_exist(self):
        with app.test_client() as c:
            article_id = 'some-invented-article-id'

            rating = {
                'user_id': 'user_id',
                'article_id': article_id,
                'upvote': True,
            }
            response = c.put(f'/articles/{article_id}', json=rating)

            assert response.status_code == 400
            assert response.json['error'] == f'Could not find article with id: {article_id}'

    def test_rate_article_returns_missing_user_id_error_when_user_id_not_provided(self):
        with app.test_client() as c:
            article_id = 'some-legit-article-id'

            rating = {
                'article_id': article_id,
                'upvote': True,
            }
            response = c.put(f'/articles/{article_id}', json=rating)

            assert response.status_code == 400
            assert response.json['error'] == 'Missing rating user id'

    def test_rate_article_returns_missing_upvote_error_when_upvote_not_provided(self):
        with app.test_client() as c:
            article_id = 'some-legit-article-id'

            rating = {
                'user_id': 'user_id',
                'article_id': article_id,
            }
            response = c.put(f'/articles/{article_id}', json=rating)

            assert response.status_code == 400
            assert response.json['error'] == 'Missing rating upvote'

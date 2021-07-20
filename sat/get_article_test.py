from hub_blog import app


class TestGetArticle:
    def test_get_article_returns_article_with_specified_article_id(self):
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
            get_response = c.get(f'/articles/{article_id}')

            assert get_response.status_code == 200
            assert get_response.json['article_id'] is not None
            assert get_response.json['title'] == article_to_create['title']
            assert get_response.json['content'] == article_to_create['content']
            assert get_response.json['tags'] == article_to_create['tags']
            assert get_response.json['user_id'] == article_to_create['user_id']
            assert get_response.json['upvotes'] == 0
            assert get_response.json['comment_ids'] == []

    def test_get_article_returns_article_not_found_exception_when_article_with_article_id_does_not_exist(self):
        with app.test_client() as c:
            article_id = 'some-invented-article-id'
            response = c.get(f'/articles/{article_id}')

            assert response.status_code == 400
            assert response.json['error'] == f'Could not find article with id: {article_id}'

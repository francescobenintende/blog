from hub_blog import app


class TestDeleteArticle:
    def test_delete_article_returns_status_ok(self):
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
            delete_response = c.delete(f'/articles/{article_id}')

            assert delete_response.status_code == 200
            assert delete_response.json == {}

    def test_delete_article_returns_article_not_found_exception_when_article_with_article_id_does_not_exist(self):
        with app.test_client() as c:
            article_id = 'some-invented-article-id'
            response = c.delete(f'/articles/{article_id}')

            assert response.status_code == 400
            assert response.json['error'] == f'Could not find article with id: {article_id}'

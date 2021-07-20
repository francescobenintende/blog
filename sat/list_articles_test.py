from hub_blog import app


class TestListArticles:
    def test_list_articles_returns_articles_with_specified_tags(self):
        with app.test_client() as c:
            article_to_create_one = {
                'title': 'Article One',
                'content': 'Lots of interesting content.',
                'tags': ['marketing'],
                'user_id': 'fran',
            }
            create_response_one = c.post('/articles', json=article_to_create_one)
            assert create_response_one.status_code == 201

            article_to_create_two = {
                'title': 'Article Two',
                'content': 'Lots of interesting content.',
                'tags': ['learning', 'marketing'],
                'user_id': 'mark',
            }
            create_response_two = c.post('/articles', json=article_to_create_two)
            assert create_response_two.status_code == 201

            article_id_one = create_response_one.json['article_id']
            article_id_two = create_response_two.json['article_id']
            list_response = c.get(f'/articles', json={'tags': ['marketing']})

            assert list_response.status_code == 200
            assert len(list_response.json) == 2
            assert article_id_one in list_response.json
            assert article_id_two in list_response.json

    def test_list_articles_returns_articles_with_specified_keywords(self):
        with app.test_client() as c:
            article_to_create_one = {
                'title': 'This is the way',
                'content': 'Lots of interesting content.',
                'tags': ['tech', 'finance'],
                'user_id': 'fran',
            }
            create_response_one = c.post('/articles', json=article_to_create_one)
            assert create_response_one.status_code == 201

            article_to_create_two = {
                'title': 'That is the way',
                'content': 'Lots of interesting content.',
                'tags': ['finance', 'travelling'],
                'user_id': 'mark',
            }
            create_response_two = c.post('/articles', json=article_to_create_two)
            assert create_response_two.status_code == 201

            article_id_one = create_response_one.json['article_id']
            article_id_two = create_response_two.json['article_id']
            list_response = c.get(f'/articles', json={'keywords': ['is', 'the', 'way']})

            assert list_response.status_code == 200
            assert len(list_response.json) == 2
            assert article_id_one in list_response.json
            assert article_id_two in list_response.json

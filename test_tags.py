from unittest import TestCase
from app import app
from models import db, User, Post, PostTag

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

test_tag = dict(name = 'test tag')

class TagTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        with app.test_client() as client:
            print()
            

    @classmethod
    def tearDownClass(cls):
        delete_tag = PostTag.query.filter_by(name = 'test tag').first()
        db.session.delete(delete_tag)
        db.session.commit()

    def test_tag_list_page(self):
        with app.test_client() as client:
            res = client.get('/tags')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Tags</h1>', html)

    def test_tag_creation_page(self):
        with app.test_client() as client:
            res = client.get('/tags/new')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Create a Tag</h1>', html)

    def test_tag_creation(self):
        with app.test_client() as client:
            res = client.post('/tags/new', data = test_tag, follow_redirects = True)
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('test tag', html)

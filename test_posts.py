from unittest import TestCase
from app import app
from models import db, User, Post

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

user = dict(first_name = 'John', last_name='Doe')
new_post = dict(title = 'Test Post', content = 'Testing Post Creation')

class PostTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        with app.test_client() as client:
            res = client.post('/users/new/add', data = user, follow_redirects = True)

    @classmethod
    def tearDownClass(cls):
        delete_post = Post.query.filter_by(title = 'Test Post').first()
        db.session.delete(delete_post)
        db.session.commit()

        delete_user = User.query.filter_by(first_name = 'John').first()
        db.session.delete(delete_user)
        db.session.commit()

    def test_new_post_page(self):
        with app.test_client() as client:
            test_user = User.query.filter_by(first_name = 'John').first()
            res = client.get(f'/users/{test_user.id}/posts/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Add Post for John Doe</h1>', html)

    def test_post_creation(self):
        with app.test_client() as client:
            test_user = User.query.filter_by(first_name = 'John').first()
            res = client.post(f'/users/{test_user.id}/posts/new/update', data = new_post, follow_redirects = True)

            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('John Doe', html)

    def test_post_details(self):
        with app.test_client() as client:
            test_post = Post.query.filter_by(title = 'Test').first()
            res = client.get(f'/posts/{test_post.id}')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Test', html)



from unittest import TestCase
from app import app
from models import db, User

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

user = dict(first_name = 'John', last_name='Doe')

class UserTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        print("INSIDE SETUP")

    @classmethod
    def tearDownClass(cls):
        delete_user = User.query.filter_by(first_name = 'John').first()
        db.session.delete(delete_user)
        db.session.commit()

    def test_user_list_page(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Blogly</h1>', html)

    def test_new_user_page(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Create a User</h1>', html)

    def test_user_creation(self):
        with app.test_client() as client:
            res = client.post('/users/new/add', data = user, follow_redirects = True)
            html = res.get_data(as_text=True)


            self.assertEqual(res.status_code, 200)
            self.assertIn('John Doe', html)

    def test_user_detais_page(self):
        with app.test_client() as client:
            search_user = User.query.filter_by(first_name = 'John').first()
            res = client.get(f'/users/details/{search_user.id}')
            html = res.get_data(as_text=True)


            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>John Doe</h1>', html)
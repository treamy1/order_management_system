import unittest
from app import app, bcrypt
from app.models import User

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

        # create a test user
        self.user = User(id='test', name='Test User', passwd=bcrypt.hashpw('test'.encode('utf-8'), bcrypt.gensalt()))
        self.user.save() # save the user to the database

    def tearDown(self):
        self.user.delete() # remove the test user from the database

    def test_login(self):
        response = self.app.post('/users/login', data=dict(id='test', passwd='test'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in successfully', response.data) # check if 'Welcome' message is present in the response

    def test_incorrct_login(self):
        response = self.app.post('/users/login', data=dict(id='test', passwd='wrong'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid ID or password', response.data) # check if 'Invalid credentials' message is present

if __name__ == '__main__':
    unittest.main()



import unittest
from app import app, bcrypt, db
from app.models import User

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

        # Establish application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Create a test user
        self.user = User(id='test', name='Test User', passwd=bcrypt.hashpw('test'.encode('utf-8'), bcrypt.gensalt()))
        db.session.add(self.user)  # Add the test user to the database
        db.session.commit()  # Commit the changes

    def tearDown(self):
        db.session.delete(self.user)  # Remove the test user from the database
        db.session.commit()
        
        # Pop the application context after teardown
        self.app_context.pop()

    def test_login(self):
        response = self.app.post('/users/login', data=dict(id='test', passwd='test'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in successfully', response.data)  # Check if 'Logged in successfully' message is present in the response

    def test_incorrect_login(self):
        response = self.app.post('/users/login', data=dict(id='test', passwd='wrong'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid ID or password', response.data)  # Check if 'Invalid ID or password' message is present in the response

if __name__ == '__main__':
    unittest.main()


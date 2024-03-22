import unittest
from app import app, bcrypt, db
from app.models import User

class SignupTestCase(unittest.TestCase):
    
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
    
    # test_signup() function tests the signup functionality, with a new user
    def test_signup(self):
        response = self.app.post('/users/signup', data=dict(id='test2', name='Test User 2', passwd='test2'), follow_redirects=True)
        self.assertEqual(response.status_code, 302) # Check if the status code is 200, which means the signup was successful
        self.assertIn(b'User created successfully', response.data)  # Check if 'User created successfully' message is present in the response
    
    # test_duplicate_signup() function tests the signup functionality, with an existing user
    def test_duplicate_signup(self):
        response = self.app.post('/users/signup', data=dict(id='test', name='Test User', passwd='test'), follow_redirects=True)
        self.assertEqual(response.status_code, 302) # Check if the status code is 200, which means the signup was unsuccessful
        self.assertIn(b'User already exists', response.data)  # Check if 'User already exists' message is present in the response

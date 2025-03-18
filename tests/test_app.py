import unittest
import os
import sys
import tempfile

# Add the parent directory to the path so we can import the application
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from website import create_app, db
from website.models import User

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and app context before each test"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database
        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create tables in the test database
        db.create_all()
        
        # Create a test user
        test_user = User(email='test@example.com', username='testuser')
        test_user.set_password('password123')
        db.session.add(test_user)
        db.session.commit()
    
    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_index_redirect(self):
        """Test the index route redirects to login for unauthenticated users"""
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_signup_page(self):
        """Test the signup page loads correctly"""
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)
    
    def test_login_page(self):
        """Test the login page loads correctly"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_valid_signup(self):
        """Test a valid user signup"""
        response = self.client.post(
            '/signup',
            data={
                'email': 'new@example.com',
                'username': 'newuser',
                'password': 'newpassword'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, newuser', response.data)
        
        # Verify user was created in database
        user = User.query.filter_by(email='new@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'newuser')
    
    def test_valid_login(self):
        """Test a valid user login"""
        response = self.client.post(
            '/login',
            data={
                'username': 'testuser',
                'password': 'password123'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, testuser', response.data)
    
    def test_invalid_login(self):
        """Test an invalid login attempt"""
        response = self.client.post(
            '/login',
            data={
                'email': 'test@example.com',
                'password': 'wrongpassword'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login unsuccessful. Please check your username and password.', response.data)
    
    def test_home_page_requires_login(self):
        """Test that the home page requires authentication"""
        response = self.client.get('/home', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def login_test_user(self):
        """Helper method to log in the test user"""
        self.client.post(
            '/login',
            data={
                'username': 'testuser',
                'password': 'password123'
            },
            follow_redirects=True
        )

    def test_home_page_with_login(self):
        """Test that the home page works with authentication"""
        # Log in the test user
        self.login_test_user()

        # Then access home page
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, testuser', response.data)

    def test_form_submission(self):
        """Test form submission for city, month, year inputs"""
        # Log in the test user
        self.login_test_user()

        # Submit the form
        response = self.client.post(
            '/home',
            data={
                'city': 'San Francisco',
                'month': 'October',
                'year': '2023'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'City: San Francisco', response.data)
        self.assertIn(b'Month: October', response.data)
        self.assertIn(b'Year: 2023', response.data)
    
    def test_logout(self):
        """Test that logout works correctly"""
        # First login
        self.client.post(
            '/login',
            data={
                'email': 'test@example.com',
                'password': 'password123'
            },
            follow_redirects=True
        )
        
        # Then logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        
        # Verify we can't access home page anymore
        response = self.client.get('/home', follow_redirects=True)
        self.assertIn(b'Login', response.data)
        self.assertNotIn(b'Welcome', response.data)

if __name__ == '__main__':
    unittest.main()
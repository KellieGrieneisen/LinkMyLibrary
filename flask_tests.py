from unittest import TestCase
from server import app, session
import flask
from model import User, connect_to_db, db
import server

class FlaskTests(TestCase):

  def setUp(self):
      """Stuff to do before every test."""

      self.client = app.test_client()
      app.config['TESTING'] = True

      

      # Connect to test database
      connect_to_db(app, "postgresql:///testlibrary")

        # Create tables and add sample data
      db.create_all()

      with self.client as c:
            with c.session_transaction() as sess:
                sess['email'] = 'tester@email.com'
      # example_data()

  def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

  def test_login_page(self):
    """Test login page."""
    result = self.client.get('/login')
    self.assertIn(b'<h1>Welcome to Link My Library!</h1>', result.data)

  def test_login(self):
    """Test login form."""
    result = self.client.post("/login",
                              data={"email": "tester@email.com", "password": "enterLib2"},
                              follow_redirects=True)
   
  def testSession1(self):
    """test if user is in session."""
  
    with self.client as c:
      res = c.get('/login')
      self.assertEqual(res.status_code, 200)
      self.assertEqual(flask.session['email'], 'tester@email.com')

  

      
  def test_homepage(self):
    """Test user homepage."""
    
    result = self.client.get('/',follow_redirects=True)

    self.assertIn(b'<title>My Library</title>', result.data)
    
  def test_logout(self):
    """Test logout button/route works."""
    res = self.client.get('/logout', follow_redirects=True)
    self.assertEqual(res.status_code, 200)
    self.assertIn(b'<h1>Welcome to Link My Library!</h1>', res.data)
    # self.assertEqual(flask.session['email'], None)

  



if __name__ == "__main__":
  # If called like a script, run our tests
  import unittest
  unittest.main()
  app.run(debug=True)
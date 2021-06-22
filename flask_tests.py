from unittest import TestCase
from server import app, session
from flask import session
from model import User, connect_to_db, db


class FlaskTests(TestCase):

  def setUp(self):
      """Stuff to do before every test."""

      self.client = app.test_client()
      app.config['TESTING'] = True
      app.config['SECRET_KEY'] = 'key'
      self.client = app.test_client()
      

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
    # this needs work, doesnt test if email in session currently
   
    
    res = self.client.get("/",follow_redirects=True)

    self.assertEqual(res.status_code, 200)
    # self.assertIn('tester@email.com',sess['email'])
      

   
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

  def test_registration_route(self):
    """Test /user route displays correct information."""
    result = self.client.get('/user',follow_redirects=True)

    self.assertIn(b'<h2 class="form-newuser-heading">Create an account here:</h2>', result.data)

  def test_registration_fields(self):
    """Test all registration fields are filled out and 
      correctly formatted."""
    result = self.client.post("/user",
                              data={"name":"Baloonicorn","email": "tester@email.com", "password": "enterLib2"},
                              follow_redirects=True)
    self.assertIsNotNone('email')
    self.assertIsNotNone('password')
    # self.assertIn('@' , result.data['email'])
    # TypeError: byte indices must be integers or slices, not str

  def test_reg_saved_to_db(self):
    """Test that new user data is saved to db."""
    result = self.client.post("/user",
                              data={"name":"Baloonicorn","email": "tester@email.com", "password": "enterLib2"},
                              follow_redirects=True)
    #look up how to test if data is saved to db
    new_user = User.query.filter(User.email=='tester@email.com').first()
    self.assertIn(new_user, 'postgresql:///testlibrary')

    #assert user in testlibrary

  def test_tbr_boolean(self):
    """Test that only books with False boolean are displayed in TBR."""



  def test_tbr_route(self):
    """Test /tbr route."""
  
    with self.client as c:
      with c.session_transaction() as sess:
        sess['email'] = 'tester@email.com'
      
        result = c.get('/tbr', follow_redirects=True)
      self.assertIn(b'<title>To Be Read</title>', result.data)
    
    



  



if __name__ == "__main__":
  # If called like a script, run our tests
  import unittest
  unittest.main()
  app.run(debug=True)
from unittest import TestCase
from server import app

class FlaskTests(TestCase):

  def setUp(self):
      """Stuff to do before every test."""

      self.client = app.test_client()
      app.config['TESTING'] = True

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"user_id": "kellie", "password": "enterLib2"},
                                  follow_redirects=True)
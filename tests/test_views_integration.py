import os
import unittest
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash

#configure app to use the testing DB
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog.database import Base, engine, session, User, Entry

class TestViews(unittest.TestCase):
    def setUp(self):
        """Test setup"""
        self.client = app.test_client()
        
        #setup tables in the DB
        Base.metadata.create_all(engine)
        
        #create example user
        self.user = User(name="ALice", email='"alice@example.com', password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()
        
    def tearDown(self):
        """test teardown"""
        session.close()
        #remove tables and their data from DB
        Base.metadata.drop_all(engine)
        
    def simulate_login(self):
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.user.id)
            http_session["_fresh"] = True
            
    def test_add_entry(self):
        self.simulate_login()
        
        response = self.client.post("/entry/add", data={"title": "Test Entry", "content": "Test content"})
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)
        
        entry = entries[0]
        self.assertEqual(entry.title, "Test Entry")
        self.assertEqual(entry.content, "Test content")
        self.assertEqual(entry.author, self.user)
        
if __name__ == "__main__":
    unittest.main()
        
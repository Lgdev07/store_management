import unittest

from src import create_app
from src.database import init_db, db

class TestCommon(unittest.TestCase):

  def setUp(self):
    self.app_instance = create_app("ConfigTest")
    self.app = self.app_instance.test_client()
    init_db(self.app_instance)

  def tearDown(self):
    with self.app_instance.app_context():
      db.session.remove()
      db.drop_all()
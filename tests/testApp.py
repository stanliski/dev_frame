import unittest
from app.models import App
from datetime import datetime
from tests import test_db


class AppModelTestCase(unittest.TestCase):

    def setUp(self):
        print 'do before test...'


    def tearDown(self):
        print 'do after test...'


    def testSave(self):

        app = App()

        app.app_name = 'test01'

        app.create_time = datetime.now()

        app.description = 'hello world'

        app.status = '1'

        test_db.session.add(app)
        test_db.session.commit()

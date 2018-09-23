import unittest
from falcon import testing
from app import App

class BasicSetUp(testing.TestCase):
    def setUp(self):
        super(BasicSetUp, self).setUp()
        a = App("db/test.sqlite3")
        self.app = a.api


class TestAppLogin(BasicSetUp):
    def test_login_get(self):
        result = self.simulate_get('/login')
        self.assertEqual(result.status_code, 405)
    def test_login_empty(self):
        result = self.simulate_post('/login')
        self.assertEqual(result.status_code, 400)
    def test_unknown_login(self):
        r = {u'username':'12',u'password':'1234'}
        result = self.simulate_post('/login',json=r)
        self.assertEqual(result.status_code, 405)
    def test_known_login(self):
        r = {u'username':'test',u'password':'1234'}
        result = self.simulate_post('/login',json=r)
        self.assertEqual(result.status_code, 200)
        self.assertNotEqual(result.cookies.get("session"),None)
        c = result.cookies.get("session").value
        self.assertEqual(len(c),64)


if __name__ == '__main__':
    unittest.main()

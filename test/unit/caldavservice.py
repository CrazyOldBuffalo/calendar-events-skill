from data import CalDAVService
import unittest


class CalDavServiceTest(unittest.TestCase):

    # tests creating a caldavservice object

    def setUp(self) -> None:
        self.caldavservice = CalDAVService("http://localhost/dav.php", "test", "password")
        self.caldavservice.connect()
        if not self.caldavservice.connect():
            self.fail("Could not connect to caldav server")

    def test_create_caldavservice(self):
        username = "username"
        password = "password"
        url = "http://localhost.com"
        caldavservice = CalDAVService(url, username, password)
        self.assertEqual(caldavservice.get_password(), username)
        self.assertEqual(caldavservice.get_password(), password)
        self.assertEqual(caldavservice.get_url(), url)

    # tests connecting to a caldav server
    def test_connect(self):
        caldavservice = CalDAVService("http://localhost/dav.php", "test", "password")
        self.assertTrue(caldavservice.connect())

    # tests failure to connect to a caldav server
    def test_connect_fail(self):
        caldavservice = CalDAVService("http://localhost/dav.php", "notusername", "notpassword")
        self.assertFalse(caldavservice.connect())

    def test_principal(self):
        self.setUp()
        self.assertIsNotNone(self.caldavservice.get_principal())

    def test_get_calendars(self):
        self.setUp()
        self.assertTrue(self.caldavservice.get_calendars())
        self.assertGreaterEqual(len(self.caldavservice.get_list_calendars(), 1))

    def test_get_events_today(self):
        self.setUp()
        self.caldavservice.`
        self.assertGreaterEqual(len(self.caldavservice.get_events_today()), 1)




if __name__ == '__main__':
    unittest.main()

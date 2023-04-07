import caldav

from data import CalDAVService
import unittest
from datetime import datetime, timedelta


class TestCalDavService(unittest.TestCase):

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
        self.assertIsInstance(self.caldavservice.get_principal(), caldav.Principal)

    def test_get_calendars(self):
        self.setUp()
        self.assertTrue(self.caldavservice.get_calendars())
        self.assertGreaterEqual(len(self.caldavservice.get_list_calendars(), 1))

    def test_get_events_today(self):
        self.setUp()
        startdate = datetime.now()
        summary = "test"
        self.caldavservice.create_event(startdate, summary)
        self.assertGreaterEqual(len(self.caldavservice.get_events_today()), 1)

    def test_get_events_date(self):
        self.setUp()
        startdate = datetime.now()
        summary = "test"
        self.caldavservice.create_event(startdate, summary)
        self.assertGreaterEqual(len(self.caldavservice.get_events_date(startdate)), 1)

    def test_create_event(self):
        self.setUp()
        startdate = datetime.now()
        summary = "test"
        test_event = self.caldavservice.create_event(startdate, summary)
        dtstart = test_event.icalendar_component.get('dtstart').dt
        dtstart = dtstart.replace(tzinfo=None)
        self.assertEquals( test_event.icalendar_component.get('summary'), summary)
        self.assertEquals(dtstart, startdate)

    def test_create_event_end(self):
        self.setUp()
        startdate = datetime.now()
        enddate = startdate + timedelta(hours=1)
        summary = "test"
        test_event = self.caldavservice.create_event(startdate, summary, enddate)
        dtstart = test_event.icalendar_component.get('dtstart').dt
        dtend = test_event.icalendar_component.get('dtend').dt
        dtstart = dtstart.replace(tzinfo=None)
        dtend = dtend.replace(tzinfo=None)
        self.assertEquals(test_event.icalendar_component.get('summary'), summary)
        self.assertEquals(test_event.icalendar_component.get('dtstart').dt, startdate)
        self.assertEquals(test_event.icalendar_component.get('dtend').dt, enddate)

    def test_get_url(self):
        self.setUp()
        self.assertEquals(self.caldavservice.get_url(), "http://localhost/dav.php")

    def test_get_username(self):
        self.setUp()
        self.assertEquals(self.caldavservice.get_username(), "test")

    def test_get_password(self):
        self.setUp()
        self.assertEquals(self.caldavservice.get_password(), "password")

    def test_get_principal(self):
        self.setUp()
        self.assertIsNotNone(self.caldavservice.get_principal())
        self.assertIsInstance(self.caldavservice.get_principal(), caldav.Principal)

if __name__ == '__main__':
    unittest.main()

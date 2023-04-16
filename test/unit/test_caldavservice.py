import caldav
import unittest
from datetime import datetime, timedelta
from data import CalDAVService


class TestCalDavService(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.flag = False
        cls.CalDAVService = CalDAVService("http://localhost/dav.php", "test", "password")
        if not cls.CalDAVService.connect() or not cls.CalDAVService.get_calendars():
            cls.flag = True

    @classmethod
    def tearDownClass(cls) -> None:
        cls.CalDAVService.closeConection()

    # tests creating a caldavservice object

    def cleanUp(self, caldavservice: CalDAVService):
        caldavservice.closeConection()

    def setUp(self) -> None:
        if self.flag:
            self.fail("Connection error")

    # Tests creating a CalDAVService object - [UT-001]
    def test_create_caldavservice(self):
        username = "username"
        password = "password"
        url = "http://localhost.com"
        caldavservice = CalDAVService(url, username, password)
        self.assertEqual(caldavservice.get_username(), username)
        self.assertEqual(caldavservice.get_password(), password)
        self.assertEqual(caldavservice.get_url(), url)

    # tests connecting to the caldav server - [UT-002]
    def test_connect(self):
        caldavservice = CalDAVService("http://localhost/dav.php", "test", "password")
        self.assertTrue(caldavservice.connect())
        self.cleanUp(caldavservice)

    # tests failure to connect to a caldav server - [UT-003]
    def test_connect_fail(self):
        caldavservice = CalDAVService("http://localhost/dav.php", "notusername", "notpassword")
        self.assertFalse(caldavservice.connect())
        self.cleanUp(caldavservice)

    # tests getting the principal of the caldav service - [UT-004]
    def test_principal(self):
        self.assertIsNotNone(self.CalDAVService.get_principal())
        self.assertIsInstance(self.CalDAVService.get_principal(), caldav.Principal)

    # tests getting the calendars of the caldav service - [UT-005]
    def test_get_calendars(self):
        self.assertTrue(self.CalDAVService.get_calendars())
        self.assertIsInstance(self.CalDAVService.get_list_calendars(), caldav.Calendar)

    # tests getting today's events from the caldav server - [UT-006]
    def test_get_events_today(self):
        startdate = datetime.now()
        summary = "test"
        self.CalDAVService.create_event(startdate, summary)
        self.assertGreaterEqual(len(self.CalDAVService.get_events_today()), 1)

    # tests getting events from the caldav server from a specific date - [UT-007]
    def test_get_events_date(self):
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day + 1
        hour = datetime.now().hour
        startdate = datetime(year, month, day, hour)
        eventdate = startdate + timedelta(hours=1)
        summary = "test"
        self.CalDAVService.create_event(eventdate, summary)
        self.assertGreaterEqual(len(self.CalDAVService.get_events_date(startdate)), 1)

    # Tests creating an event on the caldav server using the end date - [UT-008]
    def test_create_event_end(self):
        startdate = datetime.now().replace(microsecond=0)
        enddate = startdate + timedelta(hours=1)
        enddate = enddate.replace(microsecond=0)
        summary = "test"
        test_event = self.CalDAVService.create_event_end_time(startdate, enddate, summary)
        dtstart = test_event.icalendar_component.get('dtstart').dt
        dtend = test_event.icalendar_component.get('dtend').dt
        dtstart = dtstart.replace(tzinfo=None)
        dtend = dtend.replace(tzinfo=None)
        self.assertEqual(test_event.icalendar_component.get('summary'), summary)
        self.assertEqual(dtstart, startdate)
        self.assertEqual(dtend, enddate)

    # Tests creating an event on the caldav server using the duration - [UT-009]
    def test_create_event(self):
        startdate = datetime.now().replace(microsecond=0)
        summary = "test"
        test_event = self.CalDAVService.create_event(startdate, summary)
        dtstart = test_event.icalendar_component.get('dtstart').dt
        dtstart = dtstart.replace(tzinfo=None)
        self.assertEqual(test_event.icalendar_component.get('summary'), summary)
        self.assertEqual(dtstart, startdate)

    # Tests getting the URL of the caldav object - [UT-010]
    def test_get_url(self):
        self.assertEqual(self.CalDAVService.get_url(), "http://localhost/dav.php")

    # Tests getting the username of the caldav object - [UT-011]
    def test_get_username(self):
        self.assertEqual(self.CalDAVService.get_username(), "test")

    # Tests getting the password of the caldav object - [UT-012]
    def test_get_password(self):
        self.assertEqual(self.CalDAVService.get_password(), "password")


if __name__ == '__main__':
    unittest.main()

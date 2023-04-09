from data import CalDAVService
from data import EventObj
from data import IcsParser
from datetime import datetime
import sys, os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestParser(unittest.TestCase):

    def test_create_parser(self):
        parser = IcsParser()
        self.assertIsInstance(parser, IcsParser)


    def test_parse(self):
        parser = IcsParser()
        caldavservice = CalDAVService("http://localhost/dav.php", "test", "password")
        if not caldavservice.connect():
            self.fail("Connection error")
        if not caldavservice.get_calendars():
            self.fail("Calendar error")
        starttime = datetime.now().replace(microsecond=0)
        summary = "test"
        event = caldavservice.create_event(starttime, summary)
        eventobj = parser.parse(event)
        self.assertIsInstance(eventobj, EventObj)
        self.assertEqual(eventobj.get_summary(), "test")
        self.assertEqual(eventobj.get_startdate(), starttime.date())
        self.assertEqual(eventobj.get_starttime(), starttime.time())
        self.assertEqual(eventobj.get_startdatetime(), datetime(starttime))


if __name__ == '__main__':
    unittest.main()

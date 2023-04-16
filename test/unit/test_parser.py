import os
import sys
import unittest
from datetime import datetime

from data import CalDAVService
from data import EventObj
from data import IcsParser

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestParser(unittest.TestCase):

    # Tests creating a parser object - [UT-021]
    def test_create_parser(self):
        parser = IcsParser()
        self.assertIsInstance(parser, IcsParser)

    # Tests the parsing of an event - [UT-022]
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

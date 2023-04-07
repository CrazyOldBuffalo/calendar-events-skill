from data import IcsParser
from data import CalDAVService
from data import EventObj
from datetime import datetime
import unittest


class TestParser(unittest.TestCase):

    def test_create_parser(self):
        parser = IcsParser()
        self.assertIsInstance(parser, IcsParser)


    def test_parse(self):
        parser = IcsParser()
        caldavservice = CalDAVService("http://localhost/dav.php", "test", "password")
        caldavservice.connect()
        calendars = caldavservice.get_calendars()
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

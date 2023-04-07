from data import EventObj
from datetime import datetime, timedelta
import unittest


class TestEventObj(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.__startdate = datetime.now().date()
        cls.__starttime = datetime.now().time()
        cls.__enddate = cls.__startdate + timedelta(days=1)
        cls.__endtime = datetime.now().time()
        cls.__summary = "test"
        cls.__ics = "test.ics"
        cls.__event = EventObj(cls.__startdate, cls.__starttime, cls.__enddate, cls.__endtime, cls.__summary, cls.__ics)

    def createEventObj(self):
        startdate = datetime.now().date()
        starttime = datetime.now().time()
        enddate = startdate + timedelta(days=1)
        endtime = datetime.now().time()
        summary = "test"
        ics = "test.ics"
        event = EventObj(startdate, starttime, enddate, endtime, summary, ics)
        self.assertIsInstance(event, EventObj)

    def test_get_ics(self):
        self.setUp()
        self.assertEqual(self.__event.get_ics(), self.__ics)

    def test_get_startdate(self):
        self.setUp()
        self.assertEqual(self.__event.get_startdate(), self.__startdate)

    def test_get_starttime(self):
        self.setUp()
        self.assertEqual(self.__event.get_starttime(), self.__starttime)

    def test_get_enddate(self):
        self.setUp()
        self.assertEqual(self.__event.get_enddate(), self.__enddate)

    def test_get_endtime(self):
        self.setUp()
        self.assertEqual(self.__event.get_endtime(), self.__endtime)

    def test_get_summary(self):
        self.setUp()
        self.assertEqual(self.__event.get_summary(), self.__summary)

    def test_get_startdatetime(self):
        self.setUp()
        self.assertEqual(self.__event.get_startdatetime(), datetime.combine(self.__startdate, self.__starttime))

    def test_get_enddatetime(self):
        self.setUp()
        self.assertEqual(self.__event.get_enddatetime(), datetime.combine(self.__enddate, self.__endtime))


if __name__ == '__main__':
    unittest.main()

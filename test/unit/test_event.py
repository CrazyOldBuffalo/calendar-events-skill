from data import EventObj
from datetime import datetime, timedelta
import unittest


class TestEventObj(unittest.TestCase):


    # Sets up the test environment
    @classmethod
    def setUpClass(cls) -> None:
        cls.__startdate = datetime.now().date()
        cls.__starttime = datetime.now().time()
        cls.__enddate = cls.__startdate + timedelta(days=1)
        cls.__endtime = datetime.now().time()
        cls.__summary = "test"
        cls.__ics = "test.ics"
        cls.__event = EventObj(cls.__startdate, cls.__starttime, cls.__enddate, cls.__endtime, cls.__summary, cls.__ics)

    # Tests the creation of an event object - [UT-013]
    def createEventObj(self):
        startdate = datetime.now().date()
        starttime = datetime.now().time()
        enddate = startdate + timedelta(days=1)
        endtime = datetime.now().time()
        summary = "test"
        ics = "test.ics"
        event = EventObj(startdate, starttime, enddate, endtime, summary, ics)
        self.assertIsInstance(event, EventObj)

    # Tests getting the ics file of an event object - [UT-014]
    def test_get_ics(self):
        self.setUp()
        self.assertEqual(self.__event.get_ics(), self.__ics)

    # Tests getting the start date of an event object - [UT-015]
    def test_get_startdate(self):
        self.setUp()
        self.assertEqual(self.__event.get_startdate(), self.__startdate)

    # Tests getting the start time of an event object - [UT-016]
    def test_get_starttime(self):
        self.setUp()
        self.assertEqual(self.__event.get_starttime(), self.__starttime)

    # Tests getting the end date of an event object - [UT-017]
    def test_get_enddate(self):
        self.setUp()
        self.assertEqual(self.__event.get_enddate(), self.__enddate)

    # Tests getting the end time of an event object - [UT-018]
    def test_get_endtime(self):
        self.setUp()
        self.assertEqual(self.__event.get_endtime(), self.__endtime)

    # Tests getting the summary of an event object - [UT-019]
    def test_get_summary(self):
        self.setUp()
        self.assertEqual(self.__event.get_summary(), self.__summary)

    # Tests getting the start datetime of an event object - [UT-020]
    def test_get_startdatetime(self):
        self.setUp()
        self.assertEqual(self.__event.get_startdatetime(), datetime.combine(self.__startdate, self.__starttime))

    def test_get_enddatetime(self):
        self.setUp()
        self.assertEqual(self.__event.get_enddatetime(), datetime.combine(self.__enddate, self.__endtime))


if __name__ == '__main__':
    unittest.main()

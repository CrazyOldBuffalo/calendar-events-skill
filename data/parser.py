from .event import EventObj

class IcsParser:
    def __init__(self, ics) -> None:
        self.__ics = ics

    def parse(self) -> EventObj:
        starttimestamp = self.__ics.icalendar_component.get('DTSTART').dt
        endtimestamp = self.__ics.icalendar_component.get('DTEND').dt
        summary = self.__ics.icalendar_component.get('SUMMARY')
        startdate = starttimestamp.date()
        starttime = starttimestamp.time()
        enddate = endtimestamp.date()
        endtime = endtimestamp.time()
        url = self.__ics.url
        return EventObj(startdate, starttime, enddate, endtime, summary, url)

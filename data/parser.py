from .event import EventObj


class IcsParser:
    def __init__(self) -> None:
        pass

    # Parses an event object from an ics file by extracting the start date,
    # start time, end date, end time, summary and url
    # Passes the extracted data to the EventObj class to create an event object for output
    def parse(self, ics) -> EventObj:
        starttimestamp = ics.icalendar_component.get('DTSTART').dt
        endtimestamp = ics.icalendar_component.get('DTEND').dt
        summary = ics.icalendar_component.get('SUMMARY')
        startdate = starttimestamp.date()
        starttime = starttimestamp.time()
        enddate = endtimestamp.date()
        endtime = endtimestamp.time()
        url = ics.url
        return EventObj(startdate, starttime, enddate, endtime, summary, url)

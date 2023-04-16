from datetime import datetime, date, time


class EventObj:

    # Constructor for the EventObj class that takes in the event details
    def __init__(self, startdate: date, starttime: time, enddate: date, endtime: time, summary: str, ics: str) -> None:
        self.__ics = ics
        self.__startdate = startdate
        self.__starttime = starttime
        self.__enddate = enddate
        self.__endtime = endtime
        self.__summary = summary

    # Gets the ics file of the event object
    def get_ics(self) -> str:
        return self.__ics

    # Gets the start date of the event object
    def get_startdate(self) -> date:
        return self.__startdate

    # Gets the start time of the event object
    def get_starttime(self) -> time:
        return self.__starttime

    # Gets the end date of the event object
    def get_enddate(self) -> date:
        return self.__enddate

    # Gets the end time of the event object
    def get_endtime(self) -> time:
        return self.__endtime

    # Gets the summary of the event object
    def get_summary(self) -> str:
        return self.__summary

    # Gets the start datetime of the event object
    def get_startdatetime(self) -> datetime:
        return datetime.combine(self.__startdate, self.__starttime)

    # Gets the end datetime of the event object
    def get_enddatetime(self) -> datetime:
        return datetime.combine(self.__enddate, self.__endtime)

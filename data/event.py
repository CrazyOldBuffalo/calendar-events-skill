from datetime import datetime, date, time

class EventObj:
    def __init__(self, startdate : date, starttime : time, enddate : date, endtime : time, summary : str, ics : str) -> None:
        self.__ics = ics
        self.__startdate = startdate
        self.__starttime = starttime
        self.__enddate = enddate
        self.__endtime = endtime
        self.__summary = summary

    def get_ics(self) -> str:
        return self.__ics
    
    def get_startdate(self) -> date:
        return self.__startdate
    
    def get_starttime(self) -> time:
        return self.__starttime
    
    def get_enddate(self) -> date:
        return self.__enddate
    
    def get_endtime(self) -> time:
        return self.__endtime
    
    def get_summary(self) -> str:
        return self.__summary

    def get_startdatetime(self) -> datetime:
        return datetime.combine(self.__startdate, self.__starttime)
        
    def get_enddatetime(self) -> datetime:
        return datetime.combine(self.__enddate, self.__endtime)
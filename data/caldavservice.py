import caldav
from typing import Tuple
from mycroft.util.time import now_utc, to_local

class CalDAVService:

    def __init__(self, url, username, password):
        self.__username = username
        self.__password = password
        self.__url = url
    

    def connect(self) -> Tuple[caldav.Principal, None]:
        try:
            client = caldav.DAVClient(url=self.__url, username=self.__username, password=self.__password)
            my_principal = client.principal()
        except (ConnectionError, ConnectionAbortedError, ConnectionAbortedError, TimeoutError):
            return None
        return my_principal
    
    def get_calendars(self) -> caldav.Calendar:
        calendars = self.__principle.calendars()
        return calendars[0]
    
    def get_events_today(self, calendar : caldav.Calendar) -> list[caldav.Event]:
        events = calendar.search(start=to_local(now_utc()), end=to_local(now_utc().replace(hour=23, minute=59, second=58)), expand=False, event=True)
        return events

    def get_events_date(self, date: datetime) -> list[caldav.Event]:
        events = self.__calendar.date_search(date, date + timedelta(days=1))
        return events
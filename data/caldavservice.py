import caldav
from datetime import datetime
from urllib3.exceptions import MaxRetryError as E
from requests.exceptions import ConnectionError
from mycroft.util.time import now_utc, to_local

class CalDAVService:

    def __init__(self, url, username, password):
        self.__username = username
        self.__password = password
        self.__url = url
        self.__principle = None
    

    def connect(self) -> bool:
        try:
            client = caldav.DAVClient(url=self.__url, username=self.__username, password=self.__password)
            self.__principle = client.principal()
        except (ConnectionError, ConnectionRefusedError, ConnectionAbortedError, TimeoutError, E):
            return False
        return True
    
    def get_calendars(self) -> bool:
        try:
            self.__calendars = self.__principle.calendars()[0]
            return True
        except IndexError:
            return False
    
    def get_events_today(self) -> list[caldav.Event]:
        events = self.__calendars.search(start=to_local(now_utc()), end=to_local(now_utc().replace(hour=23, minute=59, second=58)), expand=False, event=True)
        return events

    def get_events_date(self, date: datetime) -> list[caldav.Event]:
        events = self.__calendars.search(start=to_local(date), end=to_local(date.replace(hour=23, minute=59, second=58)), expand=False, event=True)
        return events
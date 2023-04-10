import caldav
from datetime import datetime, timedelta
from urllib3.exceptions import MaxRetryError as E
from requests.exceptions import ConnectionError
from mycroft.util.time import now_utc, to_local


class CalDAVService:

    def __init__(self, url, username, password):
        self.__calendars = None
        self.__username = username
        self.__password = password
        self.__url = url
        self.__client = None
        self.__principal = None

    def connect(self) -> bool:
        try:
            self.__client = caldav.DAVClient(url=self.__url, username=self.__username, password=self.__password)
            self.__principal = self.__client.principal()
        except (ConnectionError, ConnectionRefusedError, ConnectionAbortedError, TimeoutError, E,
                caldav.lib.error.AuthorizationError):
            self.__principal = None
            return False
        return True

    def get_calendars(self) -> bool:
        try:
            self.__calendars = self.__principal.calendars()[0]
            return True
        except IndexError:
            return False

    def get_event_summary(self, date: datetime, summary: str) -> list[caldav.Event]:
        return self.__calendars.search(start=to_local(date),
                                       end=to_local(date.replace(hour=23, minute=59, second=58)), expand=False,
                                       event=True, summary=summary)

    def get_event_by_id(self, uid: str):
        return self.__calendars.event_by_uid(uid)

    def get_events_today(self) -> list[caldav.Event]:
        events = self.__calendars.search(start=to_local(now_utc()),
                                         end=to_local(now_utc().replace(hour=23, minute=59, second=58)), expand=False,
                                         event=True)
        return events

    def get_events_date(self, date: datetime) -> list[caldav.Event]:
        events = self.__calendars.search(start=to_local(date),
                                         end=to_local(date.replace(hour=23, minute=59, second=58)), expand=False,
                                         event=True)
        return events

    def create_event(self, startdate: datetime, summary: str) -> caldav.Event:
        event = self.__calendars.save_event(
            dtstart=startdate,
            dtend=startdate + timedelta(hours=1),
            summary=summary,
        )
        return event

    def create_event_end_time(self, startdate: datetime, enddate: datetime, summary: str) -> caldav.Event:
        event = self.__calendars.save_event(
            dtstart=startdate,
            dtend=enddate,
            summary=summary,
        )
        return event

    def delete_event(self, eventid: str) -> bool:
        event = self.get_event_by_id(eventid)
        if event is not None:
            event.delete()
            return True
        return False

    def closeConection(self):
        self.__client.close()
        self.__client.__exit__(None, None, None)

    # Getters and Setters
    def get_url(self) -> str:
        return self.__url

    def get_username(self) -> str:
        return self.__username

    def get_password(self) -> str:
        return self.__password

    def get_principal(self) -> caldav.Principal:
        return self.__principal

    def get_list_calendars(self) -> caldav.Calendar:
        return self.__calendars

    def set_url(self, url: str) -> None:
        self.__url = url

    def set_username(self, username: str) -> None:
        self.__username = username

    def set_password(self, password: str) -> None:
        self.__password = password

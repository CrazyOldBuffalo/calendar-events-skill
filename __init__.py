from datetime import datetime, timedelta
import caldav
from .data import *
from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.parse import (extract_datetime, fuzzy_match, extract_number,
                                normalize)
from mycroft.util.time import now_utc, to_local
from lingua_franca.format import nice_date_time, nice_time


class CalendarEvents(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def get_credentials(self):
        self.__url = self.settings.get("url", "http://localhost/dav.php")
        self.__username = self.settings.get('username', "test")
        self.__password = self.settings.get('password', "password")

    def initialize(self):
        self.get_credentials()
    
    def shutdown(self):
        self.speak_dialog('failed.to.execute')

    
    @intent_file_handler('events.calendar.intent')
    def handle_events_calendar(self, message):
        self.initialize()
        date = extract_datetime(message.data.get('date'))
        self.speak_dialog('events.calendar')
        self.__principle = self.connect()
        self.__calendar = self.get_calendars()
        events = self.get_events_today()
        if not events:
            self.speak_dialog('no.events', data={'date': date})
        elif len(events) == 1:
            self.one_event_today(events)
        else:
            self.multiple_events_today(events)

        
    def connect(self) -> caldav.Principal:
        try:
            client = caldav.DAVClient(url=self.__url, username=self.__username, password=self.__password)
            my_principal = client.principal()
        except (ConnectionError, ConnectionAbortedError, ConnectionAbortedError, TimeoutError):
            self.speak_dialog('connection.error')
            self.shutdown()
        self.speak("I Connected Successfully")
        return my_principal

    def get_calendars(self) -> caldav.Calendar:
        calendars = self.__principle.calendars()
        return calendars[0]

    def get_events_today(self) -> list[caldav.Event]:
        today = now_utc().replace(hour=0, minute=1, second=21)
        today_local = to_local(today)
        results = self.__calendar.search(start=today_local, end=to_local(today.replace(hour=23, minute=59, second=58)), expand=False, event =True)
        return results

    def one_event_today(self, events : list[caldav.Event]):
        event = events[0]
        parser = IcsParser(event)
        event = parser.parse()
        date = nice_time(event.get_starttime(), use_24hour=True, use_ampm=True)
        self.speak("I Found {} Event Today".format(len(events)))
        self.speak("The Event is {}".format(event.get_summary()))
        self.speak("At {}".format(date))

    def multiple_events_today(self, events : list[caldav.Event]):
        self.speak("I Found {} Events Today".format(len(events)))
        for event in events:
            parser = IcsParser(event)
            event = parser.parse()
            self.speak("The Event is called {}".format(event.get_summary()))
            self.speak("At {}".format(event))

def create_skill():
    return CalendarEvents()


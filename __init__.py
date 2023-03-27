from datetime import datetime, timedelta
import caldav
from .data import *
from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.parse import extract_datetime
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
        timeset = message.data.get('date')
        self.speak_dialog('events.calendar', wait=True)
        self.__principle = self.connect()
        self.__calendar = self.get_calendars()
        
        if 'today' in timeset:
            self.handle_events_today(timeset)
        else:
            exdate, rest = extract_datetime(timeset) or (None, None)
            if exdate is None:
                self.speak_dialog('date.error')
                self.shutdown()
            else:
                self.speak(nice_date_time(exdate, lang=self.lang, use_24hour=True, use_ampm=True), wait=True)
                self.handle_events_date(exdate)

        
    def connect(self) -> caldav.Principal:
        try:
            client = caldav.DAVClient(url=self.__url, username=self.__username, password=self.__password)
            my_principal = client.principal()
        except (ConnectionError, ConnectionAbortedError, ConnectionAbortedError, TimeoutError):
            self.speak_dialog('connection.error')
            self.shutdown()
        return my_principal


    def handle_events_today(self, date: str):
        events = self.get_events_today()
        if not events:
            self.speak_dialog('no.events', data={'date': date})
        elif len(events) == 1:
            self.one_event_today(events)
        else:
            self.multiple_events_today(events)

    def handle_events_date(self, date: datetime):
        events = self.get_events_date(date)
        if not events:
            self.speak_dialog('no.events', data={'date': nice_date_time(date, lang=self.lang, use_24hour=True, use_ampm=True)})
        elif len(events) == 1:
            self.one_event_date(events)
        else:
            self.multiple_events_date(events)
    

    def get_calendars(self) -> caldav.Calendar:
        calendars = self.__principle.calendars()
        return calendars[0]
    

    def get_events_today(self) -> list[caldav.Event]:
        today = now_utc().replace(hour=0, minute=1, second=21)
        today_local = to_local(today)
        results = self.__calendar.search(start=today_local, end=to_local(today.replace(hour=23, minute=59, second=58)), expand=False, event=True)
        return results
    
    
    def get_events_date(self, searchdate: datetime) -> list[caldav.Event]:
        results = self.__calendar.search(start=searchdate, end=searchdate.replace(hour=23, minute=59, second=58), expand=False, event=True)
        return results
    

    def one_event_today(self, events : list[caldav.Event]):
        event = events[0]
        parser = IcsParser()
        ev = parser.parse(event)
        date = nice_time(ev.get_starttime(), use_24hour=True, use_ampm=True)
        self.speak("I Found {} Event Today".format(len(events)))
        self.speak("The Event is {}".format(ev.get_summary()))
        self.speak("At {}".format(date))


    def multiple_events_today(self, events : list[caldav.Event]):
        self.speak("I Found {} Events Today".format(len(events)))
        for event in events:
            parser = IcsParser()
            ev = parser.parse(event)
            date = nice_time(ev.get_starttime(), use_24hour=True, use_ampm=True)
            self.speak("Event {}, is {}".format(events.index(event) + 1, ev.get_summary()))
            self.speak("At {}".format(date))
        
    def one_event_date(self, events : list[caldav.Event]):
        event = events[0]
        parser = IcsParser()
        ev = parser.parse(event)
        date = nice_time(ev.get_starttime(), use_24hour=True, use_ampm=True)
        self.speak("I Found {} Event".format(len(events)))
        self.speak("The Event is {}".format(ev.get_summary()))
        self.speak("At {}".format(date))

    def multiple_events_date(self, events : list[caldav.Event]):
        self.speak("I Found {} Events".format(len(events)))
        for event in events:
            parser = IcsParser()
            ev = parser.parse(event)
            date = nice_time(ev.get_starttime(), use_24hour=True, use_ampm=True)
            self.speak("Event {}, is {}".format(events.index(event) + 1, ev.get_summary()))
            self.speak("At {}".format(date))


def create_skill():
    return CalendarEvents()


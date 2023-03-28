from datetime import datetime
import caldav
from .data import *
from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.util.parse import extract_datetime
from mycroft.util.time import now_utc, to_local
from lingua_franca.format import nice_date_time, nice_time, nice_date


class CalendarEvents(MycroftSkill):


    def __init__(self):
        MycroftSkill.__init__(self)


    def get_credentials(self):
        self.__url = self.settings.get("url", "http://localhost/dav.php")
        self.__username = self.settings.get('username', "test")
        self.__password = self.settings.get('password', "password")


    def initialize(self):
        self.get_credentials()
        self.__caldavservice = CalDAVService(self.__url, self.__username, self.__password)
        self.__parser = IcsParser()


    def extract_date(self, timeset):
        exdate, rest = extract_datetime(timeset) or (None, None)
        if exdate is None:
            self.speak_dialog('date.error', wait=True)
            self.shutdown()
        else:
            return exdate
        
    @intent_handler('create.event.calendar.intent')
    def handle_create_events_calendar(self):
        self.speak_dialog('create.event.calendar', wait=True)
        self.initialize()
        if not self.__caldavservice.connect():
            self.speak_dialog('connection.error', wait=True)
            self.shutdown()
            return True
        if not self.__caldavservice.get_calendars():
            self.speak_dialog('calendar.error', wait=True)
            self.shutdown()
            return True
        self.event_creation()
        
    
    @intent_handler('events.calendar.intent')
    def handle_events_calendar(self, message):
        self.speak_dialog('events.calendar', wait=True)
        self.initialize()
        if not self.__caldavservice.connect():
            self.speak_dialog('connection.error', wait=True)
            self.shutdown()
            return True
        if not self.__caldavservice.get_calendars():
            self.speak_dialog('calendar.error', wait=True)
            self.shutdown()
            return True
        data = message.data.get('date')
        if data is None:
            self.__timeset = now_utc()
            self.__today = True
        elif 'today'.lower() in data:
            self.__today = True
            self.__timeset = self.extract_date(data)
        else:
            self.__today = False
            self.__timeset = self.extract_date(data)
        self.handle_events()

    def handle_events(self):
        events = self.__caldavservice.get_events_date(self.__timeset)
        if not events:
            self.speak_dialog('no.events', data={'date': nice_date(self.__timeset, lang=self.lang)})
        else:
            self.output_events(events)

    
    def event_creation(self):
        summary = self.get_summary()

    def get_summary(self) -> str:
        summary = self.get_response('get.summary', num_retries=2)
            




    def output_events(self, events: list[caldav.Event]):
        if self.__today:
            self.speak('You have {} event today'.format(len(events)))
        else:
            self.speak('You have {} events on {}'.format(len(events), nice_date(self.__timeset, lang=self.lang)))
        if len(events) == 1:
            ev = self.__parser.parse(events[0])
            self.speak("{}" .format(ev.get_summary()))
            self.speak("It starts at {}" .format(nice_time(ev.get_starttime(), lang=self.lang, use_24hour=False, use_ampm=True)))
        else:
            for event in events:
                ev = self.__parser.parse(event)
                self.speak("Event {}" .format(events.index(event)+1))
                self.speak("{}" .format(ev.get_summary()))
                self.speak("It starts at {}" .format(nice_time(ev.get_starttime(), lang=self.lang, use_24hour=False, use_ampm=True)))


def create_skill():
    return CalendarEvents()


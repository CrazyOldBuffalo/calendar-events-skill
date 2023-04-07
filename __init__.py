import datetime
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
            return None
        else:
            return exdate

    def connection(self) -> bool:
        if not self.__caldavservice.connect():
            self.speak_dialog('connection.error', wait=True)
            self.shutdown()
            return False
        if not self.__caldavservice.get_calendars():
            self.speak_dialog('calendar.error', wait=True)
            self.shutdown()
            return False
        self.speak("I'm Connected")
        return True

    @intent_handler('create.event.calendar.intent')
    def handle_create_events_calendar(self, message=None):
        self.speak_dialog('create.event.calendar')
        self.initialize()
        self.speak(self.__caldavservice)
        if self.__caldavservice is None:
            if not self.connection():
                return True
        created_event = self.event_creation()
        created_event = self.__parser.parse(created_event)
        self.created_event_output(created_event)

    @intent_handler('events.calendar.intent')
    def handle_events_calendar(self, message):
        self.speak_dialog('events.calendar', wait=True)
        self.initialize()
        if not self.connection():
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
        event_loop = True
        while event_loop:
            summary = self.get_response('get.summary', num_retries=2)
            date = self.get_response('date', num_retries=2)
            date = self.extract_date(date)
            if date is None:
                event_loop = False
                return False
            time = self.get_response('time', num_retries=2)
            time = self.extract_date(time)
            if time is None:
                event_loop = False
                return False
            confirmation = self.event_confirmation(summary, date, time)
            if confirmation:
                event_loop = False
                return self.__caldavservice.create_event(summary, date, time)
            elif confirmation is None:
                event_loop = False
                return False
            else:
                continue

    def event_confirmation(self, summary, date, time):
        confirmation = self.ask_yesno('event.confirmation', data={'summary': summary, 'date': date, 'time': time})
        if confirmation == 'yes':
            return True
        elif confirmation == 'no':
            return False
        else:
            return None

    def created_event_output(self, created_event: EventObj) -> None:
        event_date = nice_date(created_event.get_startdate(), lang=self.lang)
        event_time = nice_time(created_event.get_starttime(), lang=self.lang, use_24hour=False, use_ampm=True)
        self.speak_dialog('event.creation.success', data={'summary': created_event.get_summary(), 'date': event_date,
                                                          'time': event_time})

    def output_events(self, events: list[caldav.Event]):
        if self.__today:
            self.speak('You have {} event today'.format(len(events)))
        else:
            self.speak('You have {} events on {}'.format(len(events), nice_date(self.__timeset, lang=self.lang)))
        if len(events) == 1:
            ev = self.__parser.parse(events[0])
            ev_starttime = nice_time(ev.get_starttime(), lang=self.lang, use_24hour=False, use_ampm=True)
            self.speak_dialog('one.event', data={'summary': ev.get_summary(), 'date': ev_starttime})
        else:
            for event in events:
                ev = self.__parser.parse(event)
                ev_starttime = nice_time(ev.get_starttime(), lang=self.lang, use_24hour=False, use_ampm=True)
                self.speak_dialog('x.event', data={'num': events.index(event) + 1, 'summary': ev.get_summary(),
                                                   'date': ev_starttime})


def create_skill():
    return CalendarEvents()

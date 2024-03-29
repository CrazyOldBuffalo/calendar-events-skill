import datetime
import caldav
from .data import EventObj, CalDAVService, IcsParser
from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.util.parse import extract_datetime
from mycroft.util.time import now_utc, to_local
from lingua_franca.format import nice_date_time, nice_time, nice_date


class CalendarEvents(MycroftSkill):

    # Initialize the skill, sets some of the class variables and properties
    def __init__(self):
        MycroftSkill.__init__(self)
        self.__event_loop = False
        self.__url = None
        self.__username = None
        self.__password = None
        self.__caldavservice = None
        self.__parser = None

    # Gets the credentials from the user
    # Currently hardcoded, will be changed to use the Mycroft account system and a stored settings file (for privacy)
    def get_credentials(self):
        self.__url = "http://localhost/dav.php"
        self.__username = "test"
        self.__password = "password"

    # Runs when the skill is initialized, gets the credentials and creates the CalDAVService and IcsParser objects
    def initialize(self):
        self.get_credentials()
        self.__caldavservice = CalDAVService(self.__url, self.__username, self.__password)
        self.__parser = IcsParser()

    # Runs when the skill is shutdown, closes the connection to the CalDAV server
    def shutdown(self):
        self.__caldavservice.closeConection()

    # Extracts the date from the user's input using the Mycroft extract_datetime function,
    # checks if the date is valid or was able to be extracted
    def extract_date(self, timeset):
        try:
            exdate, rest = extract_datetime(timeset) or (None, None)
        except (ValueError, TypeError):
            self.speak_dialog('date.error', wait=True)
            self.shutdown()
            return None
        if exdate is None:
            self.speak_dialog('date.error', wait=True)
            self.shutdown()
            return None
        else:
            return exdate

    # Connects to the CalDAV server and gets the calendars, checks if the connection was successful
    # If unsuccessful, shuts down the skill
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

    # Event handler for the 'create.event.calendar' intent, creates an event using the event_creation function
    # If the event was created successfully, outputs the event to the user
    # checks the connection to the CalDAV server before creating the event
    # and outputs an error if the connection is unsuccessful
    @intent_file_handler('create.event.calendar.intent')
    def handle_create_events_calendar(self, message):
        self.speak_dialog('create.event.calendar', wait=True)
        self.initialize()
        if not self.connection():
            return True
        created_event = self.event_creation()
        if created_event is None:
            self.shutdown()
            return True
        elif created_event is False:
            self.shutdown()
            return True
        else:
            cr_event = self.__parser.parse(created_event)
            self.created_event_output(cr_event)

    # Event handler for the 'events.calendar' intent,
    # gets the events for a specific date using the handle_events function
    # also checks the connection to the CalDAV server before getting
    # the events and outputs an error if the connection is unsuccessful
    @intent_file_handler('events.calendar.intent')
    def handle_events_calendar(self, message):
        self.speak_dialog('events.calendar', wait=True)
        self.initialize()
        if not self.connection():
            return True
        data = message.data.get('date')
        if 'today'.lower() in data:
            self.__today = True
            self.__timeset = self.extract_date(data)
        else:
            self.__today = False
            self.__timeset = self.extract_date(data)
        if self.__timeset is None:
            return True
        self.handle_events()
        self.shutdown()

    # Gets the events for a specific date and outputs them to the user using the CalDAVService class to get the events
    # If there are no events for the date, outputs dialog otherwise runs the output_events function
    def handle_events(self):
        events = self.__caldavservice.get_events_date(self.__timeset)
        if not events:
            self.speak_dialog('no.events', data={'date': nice_date(self.__timeset, lang=self.lang)})
        else:
            self.output_events(events)

    # Creates an event using the CalDAVService class and the user's input
    # Gets the summary, date and time from the user using the Mycroft get_response function
    # and confirms the event with the user
    # If the user confirms the event, creates the event and returns the event
    # If the user cancels the event, exits the event creation loop and returns False
    # If the event details are incorrect, continues to loop until the user cancels the event or the details are correct
    # Then outputs the event to the user
    def event_creation(self):
        self.__event_loop = True
        while self.__event_loop:
            summary = self.get_response('summary', num_retries=2)
            date = self.get_response('date', num_retries=2)
            if date is None:
                self.__event_loop = False
                self.speak_dialog('event.creation.cancelled', wait=True)
                self.shutdown()
                return False
            date = self.extract_date(date)
            time = self.get_response('time', num_retries=2)
            if time is None:
                self.__event_loop = False
                self.speak_dialog('event.creation.cancelled', wait=True)
                self.shutdown()
                return False
            time = self.extract_date(time)
            if date is None or time is None:
                self.__event_loop = False
                self.speak_dialog('event.creation.error', wait=True)
                self.shutdown()
                return False
            confirmation = self.event_confirmation(summary, nice_date(date, lang=self.lang),
                                                   nice_time(time, lang=self.lang, use_24hour=False, use_ampm=True))
            if confirmation is None:
                self.__event_loop = False
                self.speak_dialog('event.creation.error', wait=True)
                self.shutdown()
                return False
            elif confirmation:
                self.__event_loop = False
                event_date = datetime.datetime.combine(date, time.time())
                event_date = to_local(event_date)
                created_event = self.__caldavservice.create_event(event_date, summary)
                if created_event.id is None:
                    self.speak_dialog('event.creation.error', wait=True)
                    self.shutdown()
                    return False
                else:
                    return created_event
            else:
                continue

    # Confirms the event with the user using the Mycroft ask_yesno function
    # If the user confirms the event, returns True
    # If the user cancels the event, returns False
    # If the user doesn't respond, returns None
    def event_confirmation(self, summary, date, time):
        confirmation = self.ask_yesno('event.confirmation', data={'summary': summary, 'date': date, 'time': time})
        if confirmation == 'yes':
            self.speak_dialog('confirmation', wait=True)
            return True
        elif confirmation == 'no':
            self.speak_dialog('retry', wait=True)
            return False
        elif confirmation is None:
            self.speak_dialog('confirmation', wait=True)
            return None
        else:
            self.speak_dialog('confirmation.error', wait=True)
            return None

    # Outputs the created event to the user using the Mycroft speak_dialog function
    # Takes the created event as an argument once parsed by the parser and is returned as an EventObj
    def created_event_output(self, created_event: EventObj) -> None:
        event_date = nice_date(created_event.get_startdate(), lang=self.lang)
        event_time = nice_time(created_event.get_starttime(), lang=self.lang, use_24hour=False, use_ampm=True)
        self.speak_dialog('event.creation.success', data={'summary': created_event.get_summary(), 'date': event_date,
                                                          'time': event_time})

    # Outputs the event/s to the user using the Mycroft speak_dialog function from the calendar events intent when
    # the user asks for their events for a specific date
    # Takes the events as an argument once parsed by the parser and is returned as a list of EventObj
    def output_events(self, events: list[caldav.Event]):
        if len(events) == 1 and self.__today:
            self.speak('You have one event today')
        elif len(events) > 1 and self.__today:
            self.speak('You have {} events today'.format(len(events)))
        elif len(events) == 1 and not self.__today:
            self.speak('You have one event on {}'.format(nice_date(self.__timeset, lang=self.lang)))
        elif len(events) > 1 and not self.__today:
            self.speak('You have {} events on {}'.format(len(events), nice_date(self.__timeset, lang=self.lang)))
        if len(events) == 1:
            ev = self.__parser.parse(events[0])
            ev_starttime = nice_time(ev.get_starttime(), lang=self.lang, use_24hour=False, use_ampm=True)
            self.speak_dialog('one.event', data={'summary': ev.get_summary(), 'time': ev_starttime})
        else:
            for event in events:
                ev = self.__parser.parse(event)
                ev_starttime = nice_time(ev.get_starttime(), lang=self.lang, use_24hour=False, use_ampm=True)
                self.speak_dialog('x.event', data={'num': events.index(event) + 1, 'summary': ev.get_summary(),
                                                   'time': ev_starttime})


def create_skill():
    return CalendarEvents()

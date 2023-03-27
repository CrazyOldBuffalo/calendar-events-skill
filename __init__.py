from mycroft import MycroftSkill, intent_file_handler
from mycroft.util import extract_datetime
import caldav


class CalendarEvents(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def get_credentials(self):
        self.url = self.settings.get("url", "http://localhost/dav.php")
        self.username = self.settings.get('username', "test")
        self.password = self.settings.get('password', "password")

    def initialize(self):
        self.get_credentials()
    
    def shutdown(self):
        self.speak_dialog('failed.to.execute')
    
    @intent_file_handler('events.calendar.intent')
    def handle_events_calendar(self, message):
        self.initialize()
        date = extract_datetime(message.data.get('date'))
        self.speak_dialog('events.calendar')
        self.principle = self.connect()

        
        
    def connect(self):
        try:
            client = caldav.DAVClient(url=self.url, username=self.username, password=self.password)
            my_principal = client.principal()
        except (ConnectionError, ConnectionAbortedError, ConnectionAbortedError, TimeoutError):
            self.speak_dialog('connection.error')
            self.shutdown()
        self.speak("I Connected Successfully")
        return my_principal



def create_skill():
    return CalendarEvents()


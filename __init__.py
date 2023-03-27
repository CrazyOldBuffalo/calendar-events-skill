from mycroft import MycroftSkill, intent_file_handler


class CalendarEvents(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('events.calendar.intent')
    def handle_events_calendar(self, message):
        date = message.data.get('date')

        self.speak_dialog('events.calendar', data={
            'date': date
        })


def create_skill():
    return CalendarEvents()


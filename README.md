# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/calendar-check.svg" card_color="#22A7F0" width="50" height="50" style="vertical-align:bottom"/> Calendar Events
Mycroft skill that allows a user to connect to their own CalDAV Server and retrieve their events from a particular date and read them out back to the user, as well as allowing them to create their own events using Mycroft and save them into the server.

## About
Skill allows the user to connect to their CalDAV Server using their credentials and using their default calendar. It allows a user to search for a particular date (Tomorrow, next monday, etc.) and will retrieve the events on that particular date if it finds any before reading them out to the user.

Also allows users to create an event on that date by asking users for the summary, the date and the time of the event and saves it to the calendar after it has been confirmed. 

> :warning: **Warning:** This implementation is aimed at a LOCAL deployment only and not designed to work over an unsecure network or via the internet.

## Setup
### CalDAV Server
In order to get this to function as intended you must have a CalDAV specification server running on your local network or on the same device as Mycroft (like using docker).
In development a Docker image running BaiKal was used.

### Skill Configuration
Within the skill settings you will need to enter the following information:
* CalDAV Server URL
* CalDAV Server Username (or the username of the account you want to use)
* CalDAV Server Password

This skill should then communicate with the server.

> :Note: **Note:** The skill works by using the default calendar on the server. If you have multiple calendars on the server you will need to change the default calendar to the one you want to use in `data/caldavservice.py` in `get_calendars()`.   
    

## Examples
* ### Searching
* "Do i have anything on {date}"
* "Is there anything in my schedule {date}"
* "What's on my agenda for {date}"
* "Do i have any events for {date}"
* ### Creating
* "Create an Event in my calendar"
* "Add an Event in my calendar"

## Credits
CrazyOldBuffalo

Cyril & Tobixen - Caldav Library (https://github.com/python-caldav/)

## Category
**Daily**
Information
Productivity

## Tags
#Calendar
#Caldav
#Events
#Schedule


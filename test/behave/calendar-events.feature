Feature: calendar-events

  Scenario: Retreive One event from the calendar today
    Given an English speaking user
    When the user says "Do i have anything on today?"
    Then "calendar-events" should reply with dialog from "events.calendar.dialog"
    Then "calendar-events" should reply with dialog from "one.event.dialog"

  Scenario Outline: Retreive One event from the calendar from a specific date
    Given an English speaking user
    When the user says "Do i have anything on <event>?"
    Then "calendar-events" should reply with dialog from "events.calendar.dialog"
    Then "calendar-events" should reply with dialog from "one.event.dialog"

    Examples:
      | event |
      | tomorrow |
      | next Wednesday |
      | 12th of December |
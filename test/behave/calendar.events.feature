Feature: calendar-events
  Background:
    given: a user has a calendar server running on their local network
    and: the user has configured their settings correctly

    Scenario: user retrieves one event from their calendar server for today
      given: the user has an event on their calendar server
        and: the user is an english speaker
        when: the user says "Do i have any events for today?"
        then: "calendar-events-skill" should respond with dialog from "one.event.dialog"

    Scenario Outline: user retrieves one event from their calendar server for a specific date
      given: the user has an event on their calendar server
        and: the user is an english speaker
        when: the user says "Do i have any events for <date>?"
        then: "calendar-events-skill" should respond with dialog from "one.event.dialog"
    
      Examples:
        | date       |
        | tomorrow   |
        | next Monday  |
        | December 12th |
      



Feature: calendar-events
  Background:
    given: a user has a calendar server running on their local network
    and: the user has configured their settings correctly
    and: the user has one event in their calendar

    Scenario: Users gets one event for the day
      given: an English speaking user
      and: the user has one event in their calendar for today
        when: the user says "do I have any events today"
        then: "calendar-events" should respond with dialog from "one.event"

    Scenario: Users gets multiple events for the day
      given: an English speaking user
      and: the user has multiple events in their calendar for today
        when: the user says "do I have any events today"
        then: "calendar-events" should respond with dialog from "x.event"

    Scenario: Users gets no events for the day
      given: an English speaking user
      and: the user has no events in their calendar for today
        when: the user says "do I have any events today"
        then: "calendar-events" should respond with dialog from "no.events"

    Scenario Outline: User gets one event from a specific date
      given: an English speaking user
      and: the user has one event in their calendar for a specific date
        when: the user says "do I have any events on <date>"
        then: "calendar-events" should respond with dialog from "one.event"

    Examples:
      | Tomorrow |
      | Next Monday |
      | The 15th of December |

    Scenario Outline: User gets multiple events from a specific date
      given: an English speaking user
      and: the user has multiple events in their calendar for a specific date
        when: the user says "do I have any events on <date>"
        then: "calendar-events" should respond with dialog from "x.event"

    Examples:
        | Tomorrow |
        | Next Monday |
        | The 15th of December |

    Scenario Outline: User gets no events from a specific date
        given: an English speaking user
        and: the user has no events in their calendar for a specific date
            when: the user says "do I have any events on <date>"
            then: "calendar-events" should respond with dialog from "no.events"

    Examples:
        | Tomorrow |
        | Next Monday |
        | The 15th of December |

  Scenario: User wants to create an event
    given: an English speaking user
      when: the user says "add an event to my calendar"
      then: "calendar-events" should respond with dialog from "create.event.calendar"
        and: "calendar-events" should respond with dialog from "get.summary"
        and: the user says "<summary>"
        then: "calendar-events" should respond with dialog from "confirmation"
        and: the user responds with "yes"
        then: "calendar-events" should respond with dialog from "date"
        and: the user says "<date>"
        then: "calendar-events" should respond with dialog from "confirmation"
        and: the user responds with "yes"
        then: "calendar-events" should respond with dialog from "time"
        and: the user says "<time>>"
        then: "calendar-events" should respond with dialog from "confirmation"
        and: the user responds with "yes"
        then: "calendar-events" should respond with dialog from "event.confirmation"
        and: and the user says "yes"
        and: "calendar-events" should respond with dialog from "event.creation.success"

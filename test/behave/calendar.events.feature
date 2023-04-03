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


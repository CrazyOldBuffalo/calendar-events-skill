Feature: calendar-events

  Scenario Outline: Retreive One event from the calendar from a specific date
    Given an English speaking user
    When the user says "Do i have anything on <event>?"
    Then "calendar-events" should reply with dialog from "events.calendar.dialog"
    Then "calendar-events" should reply with dialog from "one.event.dialog"

    Examples:
      | event |
      | next Tuesday |
      | next Wednesday |

  Scenario Outline: Retreieve Multiple events from the calendar for a specific date
    Given an English speaking user
    When the user says "Do i have anything on <event>?"
    Then "calendar-events" should reply with dialog from "events.calendar.dialog"
    Then "calendar-events" should reply with dialog from "x.event.dialog"

    Examples:
      | event |
      | today |
      | tomorrow |

  Scenario Outline: Retrieve no events from the calendar for a specific date
    Given an English speaking user
    When the user says "Do i have anything on <event>?"
    Then "calendar-events" should reply with dialog from "events.calendar.dialog"
    Then "calendar-events" should reply with dialog from "no.events.dialog"

    Examples:
      | event |
      | 17th of August |
      | 12th of December |

  Scenario Outline: User asks for a non date
    Given an English speaking user
    When the user says "Do i have anything on <event>?"
    Then "calendar-events" should reply with dialog from "events.calendar.dialog"
    And "calendar-events" should reply with dialog from "date.error.dialog"

    Examples:
      | event |
      | Bacon |
      | Turtle |

  Scenario Outline: User creates am event in their calendar
    Given an English speaking user
    When the user says "Create an event in my calendar"
    Then "calendar-events" should reply with dialog from "create.event.calendar.dialog"
    And "calendar-events" should reply with dialog from "summary.dialog"
    Then the user says "<event>"
    And "calendar-events" should reply with dialog from "date.dialog"
    Then the user says "<date>"
    And "calendar-events" should reply with dialog from "time.dialog"
    Then the user says "<time>"
    And "calendar-events" should reply with dialog from "event.confirmation.dialog"
    Then the user says "yes"
    And "calendar-events" should reply with dialog from "event.creation.success.dialog"

    Examples:
      | event | date | time |
      | Meeting | 17th of August | 12:00pm |
      | Dinner | 12th of December | 19:00 |

  Scenario Outline: User creates an event in their calendar but doesn't confirm
    Given an English speaking user
    When the user says "Create an event in my calendar"
    Then "calendar-events" should reply with dialog from "create.event.calendar.dialog"
    And "calendar-events" should reply with dialog from "summary.dialog"
    Then the user says "<event>"
    And "calendar-events" should reply with dialog from "date.dialog"
    Then the user says "<date>"
    And "calendar-events" should reply with dialog from "time.dialog"
    Then the user says "<time>"
    And "calendar-events" should reply with dialog from "event.confirmation.dialog"
    Then the user says "no"
    And "calendar-events" should reply with dialog from "retry.dialog"
    And "calendar-events" should reply with dialog from "summary.dialog"
    Then the user says "<event>"
    And "calendar-events" should reply with dialog from "date.dialog"
    Then the user says "<date>"
    And "calendar-events" should reply with dialog from "time.dialog"
    Then the user says "<time>"
    And "calendar-events" should reply with dialog from "event.confirmation.dialog"
    Then the user says "yes"
    And "calendar-events" should reply with dialog from "event.creation.success.dialog"

    Examples:
      | event | date | time |
      | Meeting | 17th of August | 12:00pm |
      | Dinner | 12th of December | 19:00 |

  Scenario Outline: User creates an event in their calendar but cancels
    Given an English speaking user
    When the user says "Create an event in my calendar"
    Then "calendar-events" should reply with dialog from "create.event.calendar.dialog"
    And "calendar-events" should reply with dialog from "summary.dialog"
    Then the user says "<event>"
    And "calendar-events" should reply with dialog from "date.dialog"
    Then the user says "<date>"
    And "calendar-events" should reply with dialog from "time.dialog"
    Then the user says "<time>"
    And "calendar-events" should reply with dialog from "event.confirmation.dialog"
    Then the user says "cancel"
    And "calendar-events" should reply with dialog from "event.creation.error.dialog"

    Examples:
      | event | date | time |
      | Meeting | 17th of August | 12:00pm |
      | Dinner | 12th of December | 19:00 |

  Scenario Outline: User creates an event in their calendar but cancels time
    Given an English speaking user
    When the user says "Create an event in my calendar"
    Then "calendar-events" should reply with dialog from "create.event.calendar.dialog"
    And "calendar-events" should reply with dialog from "summary.dialog"
    Then the user says "<event>"
    And "calendar-events" should reply with dialog from "date.dialog"
    Then the user says "<date>"
    And "calendar-events" should reply with dialog from "time.dialog"
    Then the user says "cancel"
    And "calendar-events" should reply with dialog from "event.creation.cancelled.dialog"

    Examples:
      | event | date |
      | Meeting | 17th of August |
      | Dinner | 12th of December |

  Scenario Outline: User creates an event in their calendar but cancels date
    Given an English speaking user
    When the user says "Create an event in my calendar"
    Then "calendar-events" should reply with dialog from "create.event.calendar.dialog"
    And "calendar-events" should reply with dialog from "summary.dialog"
    Then the user says "<event>"
    And "calendar-events" should reply with dialog from "date.dialog"
    Then the user says "cancel"
    And "calendar-events" should reply with dialog from "event.creation.cancelled.dialog"

    Examples:
      | event |
      | Meeting |
      | Dinner |

  

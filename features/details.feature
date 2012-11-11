Feature: Object details
    Testing the details function

    Scenario: Details via place id
        When looking up place 1758375
        Then a HTTP 200 is returned


    Scenario Outline: Details via OSM id
        When looking up osm <type> <id>
        Then a HTTP 200 is returned

    Examples:
     | type | id
     | N    | 158845944
     | W    | 72493656
     | R    | 62422


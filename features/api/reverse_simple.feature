Feature: Simple Reverse Tests
    Simple tests for internal server errors and response format.
    These tests should pass on any Nominatim installation.

    Scenario Outline: Simple reverse-geocoding
        When looking up coordinates <lat>,<lon>
        Then a valid response is returned
        Given format xml
        Then a valid response is returned
        Given format json
        Then a valid response is returned
        Given format jsonv2
        Then a valid response is returned

    Examples:
     | lat      | lon
     | 0.0      | 0.0
     | 45.3     | 3.5
     | -79.34   | 23.5
     | 0.23     | -178.555

    Scenario: Wrapping of legal jsonp requests
        When looking up coordinates 67.3245,0.456
        With parameter json_callback as "foo"
        And format "json"
        Then a valid response is returned
        And format "jsonv2"
        Then a valid response is returned

    Scenario Outline: Reverse-geocoding with paramters
        When looking up coordinates 67.3245,0.456
        With parameter <parameters> as "<value>"
        Given format xml
        Then a valid response is returned
        Given format json
        Then a valid response is returned
        Given format jsonv2
        Then a valid response is returned

   Examples:
     | parameters        | value
     | addressdetails    | 1
     | polygon           | 1
     | accept-language   | de,en
     | zoom              | 10

Feature: Simple Reverse Tests
    Simple tests for internal server errors and response format.
    These tests should pass on any Nominatim installation.

    Scenario Outline: Simple reverse-geocoding
        When looking up coordinates <lat>,<lon>
        Then valid xml is returned
        Given format xml
        Then valid xml is returned
        Given format json
        Then valid json is returned
        Given format jsonv2
        Then valid json is returned

    Examples:
     | lat      | lon
     | 0.0      | 0.0
     | 45.3     | 3.5
     | -79.34   | 23.5
     | 0.23     | -178.555

    Scenario: Wrapping of legal jsonp requests
        When looking up coordinates 67.3245,0.456
        With parameters "json_callback=foo&format=json"
        Then valid json is returned

    Scenario Outline: Reverse-geocoding with paramters
        When looking up coordinates 67.3245,0.456
        With parameters "<parameters>"
        Then valid xml is returned
        Given format xml
        Then valid xml is returned
        Given format json
        Then valid json is returned
        Given format jsonv2
        Then valid json is returned

   Examples:
     | parameters
     | addressdetails=1
     | polygon=1
     | accept-language=de,en
     | zoom=10

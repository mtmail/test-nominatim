Feature: Simple Tests
    Simple tests for internal server errors.
    These tests should pass on any Nominatim installation.

    Scenario Outline: Simple Searches
        When searching for "<query>"
        Then valid html is returned
        Using format html
        Then valid html is returned
        Using format xml 
        Then valid xml is returned
        Using format json
        Then valid json is returned
        Using format jsonv2
        Then valid json is returned

    Examples:
     | query
     | New York, New York
     | France
     | 12, Main Street, Houston
     | München
     | 東京都
     | hotels in nantes
     | xywxkrf

    Scenario: Wrapping of legal jsonp requests
        When searching for "Tokyo"
        With parameters "json_callback=foo&format=json"
        Then the result is wrapped in function foo

    Scenario Outline: Searches with different parameters
        When searching for "Manchester"
        With parameters "<parameters>"
        Using format html
        Then valid html is returned
        Using format xml 
        Then valid xml is returned
        Using format json
        Then valid json is returned
        Using format jsonv2
        Then valid json is returned

    Examples:
     | parameters
     | addressdetails=1
     | polygon=1
     | polygon_text=1
     | polygon_kml=1
     | polygon_geojson=1
     | polygon_svg=1
     | accept-language=de,en
     | countrycodes=uk,ir
     | viewbox=12.59,52.78,14.19,52.25
     | bounded=1
     | exclude_place_ids=385252,1234515
     | limit=1000
     | dedupe=1

    Scenario Outline: Simple reverse-geocoding
        When looking up coordinates <lat>,<lon>
        Then valid xml is returned
        Using format xml 
        Then valid xml is returned
        Using format json
        Then valid json is returned
        Using format jsonv2
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
        Then the result is wrapped in function foo

    Scenario Outline: Reverse-geodocing with paramters
        When looking up coordinates 67.3245,0.456
        With parameters "<parameters>"
        Then valid xml is returned
        Using format xml 
        Then valid xml is returned
        Using format json
        Then valid json is returned
        Using format jsonv2
        Then valid json is returned

   Examples:
     | parameters
     | addressdetails=1
     | polygon=1
     | accept-language=de,en
     | zoom=10

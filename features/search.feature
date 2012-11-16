Feature: Geocoding
    Testing the search function

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


     # bug https://trac.openstreetmap.org/ticket/4683
     Scenario: limit=1 returns something
        When searching for "Hamburg"
        With parameters "limit=1"
        Then exactly 1 result is returned

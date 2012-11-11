Feature: Geocoding
    Testing the search function

    Scenario Outline: Simple Searches
        When searching for "<query>"
        Then a HTTP 200 is returned
        Using format html
        Then a HTTP 200 is returned
        Using format xml 
        Then a HTTP 200 is returned
        Using format json
        Then a HTTP 200 is returned
        Using format jsonv2
        Then a HTTP 200 is returned

    Examples:
     | query
     | New York, New York
     | France
     | 12, Main Street, Houston
     | München
     | 東京都


    Scenario Outline: Searches with different parameters
        When searching for "Manchester"
        With parameters "<parameters>"
        Using format html
        Then a HTTP 200 is returned
        Using format xml 
        Then a HTTP 200 is returned
        Using format json
        Then a HTTP 200 is returned
        Using format jsonv2
        Then a HTTP 200 is returned

    Examples:
     | parameters
     | addressdetails=1
     | polygon=1
     | polygon_text=1
     | polygon_kml=1
     | polygon_geojson=1
     | polygon_svg=1
     | json_callback=foobar
     | accept-language=de,en
     | countrycodes=uk,ir
     | viewbox=12.59,52.78,14.19,52.25
     | bounded=1
     | exclude_place_ids=385252,1234515
     | limit=1000
     | dedupe=1
     | debug=1

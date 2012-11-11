Feature: Reverse geocoding
    Testing the reverse function

    Scenario Outline: Simple reverse-geocoding
        When looking up coordinates <lat>,<lon>
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
     | lat      | lon
     | 0.0      | 0.0
     | 45.3     | 3.5
     | -79.34   | 23.5
     | 0.23     | -178.555


    Scenario Outline: Reverse-geodocing with paramters
        When looking up coordinates 67.3245,0.456
        With parameters "<parameters>"
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
     | parameters
     | addressdetails=1
     | polygon=1
     | json_callback=foobar
     | accept-language=de,en
     | zoom=10

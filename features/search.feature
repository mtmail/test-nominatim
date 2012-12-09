Feature: Geocoding
    Testing the search function

     # bug https://trac.openstreetmap.org/ticket/4683
     Scenario: limit=1 returns something
        When searching for "Hamburg"
        With parameters "limit=1"
        Then exactly 1 result is returned

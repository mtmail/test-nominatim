Feature: Geocoding
    Testing the search function

    Scenario: node type - place node only
        When searching for "Plymouth, Montserrat"
        Then result 1 is within 16.4750,17.0153,-62.4507,-61.9354
        And then result 1 is of type node

    Scenario: rel type - town with admin boundaries
        When searching for "Bern, Switzerland"
        Then result 1 is within 45.8,47.8,5.9,10.5
        And then result 1 is of type relation

    Scenario: way type - simple road
        When searching for "Avenue des Champs-Elysées, Paris"
        Then result 1 is within 48.8155,48.9021,2.2241,2.4697
        And then result 1 is of type way

    Scenario: node type - house number
        When searching for "Rosalind St 4, Sydney"
        Then at least 1 result is returned

    # bug https://trac.openstreetmap.org/ticket/4683
    Scenario: limit=1 returns something
        When searching for "Hamburg"
        With parameters "limit=1"
        Then exactly 1 result is returned

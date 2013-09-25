Feature: Structured search queries
    Testing correctness of results with
    structured queries

    Scenario: Country only
        When searching for the following:
          | type       | value
          | country    | Canada
        Given parameter addressdetails as "1"
        Then xml result 1 has address details in order country,country_code

    Scenario: Postcode only
        When searching for the following:
          | type       | value
          | postalcode | GU2 7UP
        Given parameter addressdetails as "1"
        Then result 1 has attribute class as "place"
        And result 1 has attribute type as "postcode"



    Scenario: Street, postcode and country
        When searching for the following:
          | type       | value
          | street     | Old Palace Road
          | postalcode | GU2 7UP
          | country    | United Kingdom
        Then at least 1 result is returned

Feature: Structured search queries
    Testing correctness of results with
    structured queries

    Scenario: Country only
        When searching for the following:
          | type       | value
          | country    | Canada
        Then result 1 contains country "Canada"


    Scenario: Street, postcode and country
        When searching for the following:
          | type       | value
          | street     | Old Palace Road
          | postalcode | GU2 7UP
          | country    | United Kingdom
        Then at least 1 result is returned

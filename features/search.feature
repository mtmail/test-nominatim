Feature: Search queries
    Testing correctness of results

    Scenario: UK House number search
        When searching for "27 Thoresby Road, Broxtowe"
        Then address 1 contains the following:
          | type         | value
          | house_number | 27
          | road         | Thoresby Road
          | city         | Broxtowe
          | state        | England
          | country      | United Kingdom
          | country_code | gb


    Scenario: House number search with address attached to landuse
        When searching for "14 Ashleigh Grove, Galway"
        Given language "en"
        Then address 1 contains the following:
          | type         | value
          | house_number | 14
          | residential  | Ashleigh Grove
          | city         | Galway
          | country      | Ireland
          | country_code | ie
        And address 1 has details without type road

    Scenario: House number interpolation even
        When searching for "140 rue Don Bosco, Saguenay"
        Given language "en"
        Then address 1 contains the following:
          | type         | value
          | house_number | 140
          | road         | rue Don Bosco
          | city         | Saguenay
          | state        | Quebec
          | country      | Canada
          | country_code | ca

    Scenario: House number interpolation odd
        When searching for "141 rue Don Bosco, Saguenay"
        Given language "en"
        Then address 1 contains the following:
          | type         | value
          | house_number | 141
          | road         | rue Don Bosco
          | city         | Saguenay
          | state        | Quebec
          | country      | Canada
          | country_code | ca

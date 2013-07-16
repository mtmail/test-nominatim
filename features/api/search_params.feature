Feature: Search queries
    Testing different queries and parameters

    Scenario: Simple XML search
        When searching for "Schaan"
        Then at least 1 xml result is returned
        And xml result 1 has attributes place_id,osm_type,osm_id
        And xml result 1 has attributes place_rank,boundingbox
        And xml result 1 has attributes lat,lon,display_name
        And xml result 1 has attributes class,type,importance,icon

    Scenario: Simple JSON search
        When searching for "Vaduz"
        Then at least 1 result is returned
        And result 1 has attributes place_id,licence,icon,class,type
        And result 1 has attributes osm_type,osm_id,boundingbox
        And result 1 has attributes lat,lon,display_name,importance
        And result 1 has not attributes address

    Scenario: JSON search with addressdetails
        When searching for "Montevideo"
        Given parameter addressdetails as "1"
        Then result 1 has address details with "Uruguay"
        And result 1 has address details in order city,state,country,country_code

    Scenario: Disabling deduplication
        When searching for "Oxford Street, London"
        Given parameter dedupe as "1"
        Then there are no duplicates
        Given parameter dedupe as "0"
        Then there are duplicates

    Scenario: Search with bounded viewbox in right area
        When searching for "restaurant"
        Given parameter bounded as "1"
        And parameter viewbox as "-87.7,41.9,-87.57,41.85"
        Then result 1 is in "Chicago"

    Scenario: Search with bounded viewboxlbrt in right area
        When searching for "restaurant"
        Given parameter bounded as "1"
        And parameter viewboxlbrt as "-87.7,41.85,-87.57,41.9"
        Then result 1 is in "Chicago"

    Scenario: No POI search with unbounded viewbox
        When searching for "restaurant"
        And parameter viewbox as "-87.7,41.9,-87.57,41.85"
        Then name of result 1 contains "restaurant"

    Scenario: Prefer results within viewbox
        When searching for "royan"
        And parameter accept-language as "en"
        Then result 1 is in "France"    
        When searching for "royan"
        And parameter viewbox as "51.94,36.59,51.99,36.56"
        And parameter accept-language as "en"
        Then result 1 is in "Iran"    

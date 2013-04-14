Feature: Search queries
    Testing different queries and parameters

    Scenario: Simple json Search
        When searching for "Vaduz"
        Then at least 1 result is returned
        And result 1 has attributes place_id,licence,icon,class,type
        And result 1 has attributes osm_type,osm_id,boundingbox
        And result 1 has attributes lat,lon,display_name,importance

    Scenario: Disabling deduplication
        When searching for "Oxford Street, London"
        Given parameter dedupe as "1"
        Then there are no duplicates
        Given parameter dedupe as "0"
        Then there are duplicates

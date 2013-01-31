Feature: Result order for Geocoding
    Testing that importance ordering returns sensible results

    Scenario Outline: city order in street search
        When searching for "<street>, <city>"
        Then result 1 contains city "<city>"

    Examples:
        | city            | street
        | Zürich          | Rigistr
        | Karlsruhe       | Lessingstr
        | München         | Karlstr
        | Praha           | Dlouhá

    Scenario Outline: use more important city in street search
        When searching for "<street>, <city>"
        Then result 1 contains country_code "<country>"

    Examples:
        | country | city       | street
        | gb      | London     | Main St
        | gb      | Manchester | Central Street

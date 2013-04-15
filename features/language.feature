Feature: Localization of search results

    Scenario: Search - default language
        When searching for "Germany"
        Then result 1 starts with "Deutschland"

    Scenario: Search - accept-language first
        When searching for "Deutschland"
        Using language "en,de"
        Then result 1 starts with "Germany"

    Scenario: Search - accept-language missing
        When searching for "Deutschland"
        Using language "xx,fr,en,de"
        Then result 1 starts with "Allemagne"

    Scenario: Search - http accept language header first
        When searching for "Deutschland"
        Using language header "fr-ca,fr;q=0.8,en-ca;q=0.5,en;q=0.3"
        Then result 1 starts with "Allemagne"

    Scenario: Search - http accept language header and accept-language
        When searching for "Germany"
        Using language header "fr-ca,fr;q=0.8,en-ca;q=0.5,en;q=0.3"
        Using language "de,en"
        Then result 1 starts with "Deutschland"

    Scenario: Search - http accept language header fallback
        When searching for "Deutschland"
        Using language header "fr-ca,en-ca;q=0.5"
        Then result 1 starts with "Allemagne"

    Scenario: Search - http accept language header fallback (upper case)
        When searching for "Deutschland"
        Using language header "fr-FR;q=0.8,en-ca;q=0.5"
        Then result 1 starts with "Allemagne"

    Scenario: Reverse - default language
        When looking up coordinates 48.13921,11.57328
        Then the address contains county "München"

    Scenario: Reverse - accept-language parameter
        When looking up coordinates 48.13921,11.57328
        Using language "en,fr"
        Then the address contains county "Munich"

    Scenario: Reverse - HTTP accept language header
        When looking up coordinates 48.13921,11.57328
        Using language header "fr-ca,fr;q=0.8,en-ca;q=0.5,en;q=0.3"
        Then the address contains county "Munich"

    Scenario: Reverse - accept-language parameter and HTTP header
        When looking up coordinates 48.13921,11.57328
        Using language header "fr-ca,fr;q=0.8,en-ca;q=0.5,en;q=0.3"
        Using language "it"
        Then the address contains county "Monaco di Baviera"


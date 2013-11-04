Feature: Reverse geocoding
    Testing the reverse function

    # Make sure country is not overwritten by the postcode
    Scenario: Country is returned
        When looking up coordinates 53.9788769,13.0830313
        Using language "de"
        Then the location address contains country "Deutschland"


from lettuce import *


@step('valid search xml is returned')
def search_validate_xml(step):
    world.call()
    assert world.results.nodeName == "searchresults", \
            "Unexpected element '%s'" % world.results.nodeName
    assert world.results.hasAttribute('attribution')
    assert world.results.hasAttribute('timestamp')
    assert world.results.hasAttribute('querystring')
    assert world.results.hasAttribute('more_url')

from nose.tools import assert_raises_regexp
import urllib
import urllib2
from lettuce import *

@step('Then a HTTP (\d+) is returned')
def send_request(step, http_code='200'):
    data = urllib.urlencode(world.params)
    url = "%s/%s?%s" % (world.base_url, world.requesttype, data)
    if http_code == '200':
        urllib2.urlopen(url)
    else:
        with assert_raises_regexp(urllib2.HTTPError, http_code):
            urllib2.urlopen(url)


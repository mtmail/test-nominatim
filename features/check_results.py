from nose.tools import assert_raises_regexp
import urllib
import urllib2
from lettuce import *
from tidylib import tidy_document

@step('Then a HTTP (\d+) is returned')
def send_request(step, http_code='200'):
    data = urllib.urlencode(world.params)
    url = "%s/%s?%s" % (world.base_url, world.requesttype, data)
    if http_code == '200':
        fd = urllib2.urlopen(url)
        world.page = fd.read()
    else:
        with assert_raises_regexp(urllib2.HTTPError, http_code):
            urllib2.urlopen(url)

@step('Then valid html is returned')
def validate_html_format(step):
    send_request(step)

    document, errors = tidy_document(world.page, options={'char-encoding' : 'utf8'})
    assert(len(errors) == 0), "Errors found in HTML document:\n%s" % errors
    world.page = document

@step('Then valid xml is returned')
def validate_xml_format(step):
    send_request(step)

@step('Then valid json is returned')
def validate_json_format(step):
    send_request(step)


@step('Then (.+) (\d+) result is returned')
def validate_result_number(step, operator, number):
    world.params['format'] = 'json'
    validate_json_format(step)

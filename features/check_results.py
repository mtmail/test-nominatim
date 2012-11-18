from nose.tools import assert_raises_regexp
import urllib
import urllib2
from lettuce import *
from tidylib import tidy_document
import json
from xml.dom.minidom import parseString

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
    world.results = document


@step('Then valid xml is returned')
def validate_xml_format(step):
    send_request(step)
    world.results = parseString(world.page)


@step('Then valid json is returned')
def validate_json_format(step):
    send_request(step)
    world.results = json.loads(world.page)

@step('Then the result is wrapped in function (.*)')
def check_for_jsonp_wrapper(step, funcname):
    world.params['format'] = 'json'
    send_request(step)
    assert world.page.startswith(funcname + '(')
    assert world.page.endswith(')')
    world.results = json.loads(world.page[(len(funcname)+1):-1])
    

@step('Then (.+) (\d+) results? is returned')
def validate_result_number(step, operator, number):
    number = int(number)
    world.params['format'] = 'json'
    validate_json_format(step)
    numres = len(world.results)
    if operator == 'less than':
        comp = numres < number
    elif operator == 'more than':
        comp = numres > number
    elif operator == 'exactly':
        comp = numres == number
    elif operator == 'at least':
        comp = numres >= number
    elif operator == 'at most':
        comp = numres <= number
    else:
        raise Error("unknown operator")

    assert comp, "Bad number of results: expected %s %d, got %d." % (operator, number, numres)

@step('Then result (\d+) starts with "(.*)"')
def validate_display_name_start(step, resnum, result):
    validate_result_number(step, 'at least', resnum)
    assert world.results[int(resnum)-1]['display_name'].startswith(result), "Expected result to start with '%s', got '%s'." % (result, world.results[int(resnum)-1]['display_name'])

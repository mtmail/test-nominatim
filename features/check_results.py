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
    req = urllib2.Request(url="%s/%s?%s" % (world.base_url, world.requesttype, data),
                          headers=world.header)
    if http_code == '200':
        fd = urllib2.urlopen(req)
        world.page = fd.read()
    else:
        with assert_raises_regexp(urllib2.HTTPError, http_code):
            urllib2.urlopen(req)

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
    

########### For search only #################

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


########## For reverse only ###############

@step('Then a valid address is returned')
def validate_reverse_hasresult(step):
    world.params['format'] = 'json'
    validate_json_format(step)

@step('Then the address contains (.*) "(.*)"')
def validate_reverse_address(step, addresstype, addressvalue):
    validate_reverse_hasresult(step)
    assert addresstype in world.results['address'], "Expected address to contain '%s'. Got %s." % (addresstype, world.results['address'])
    assert world.results['address'][addresstype] == addressvalue, "Expected address '%s' to be '%s'. Got %s." % (addresstype, addressvalue, world.results['address'][addresstype])

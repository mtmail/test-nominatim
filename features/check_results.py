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
def run_validate_display_name_start(step, resnum, result):
    validate_result_number(step, 'at least', resnum)
    validate_display_name_start(step, resnum, result)

@step('And then result (\d+) starts with "(.*)"')
def validate_display_name_start(step, resnum, result):
    assert world.results[int(resnum)-1]['display_name'].startswith(result), "Expected result to start with '%s', got '%s'." % (result, world.results[int(resnum)-1]['display_name'])

@step('Then result (\d+) is within ([-.\d]+),([-.\d]+),([-.\d]+),([-.\d]+)')
def run_validate_search_coordinates(step, resnum, latmin, latmax, lonmin, lonmax):
    validate_result_number(step, 'at least', resnum)
    validate_search_coordinates(step, resnum, latmin, latmax, lonmin, lonmax)

@step('And then result (\d+) is within ([-.\d]+),([-.\d]+),([-.\d]+),([-.\d]+)')
def validate_search_coordinates(step, resnum, latmin, latmax, lonmin, lonmax):
    res = world.results[int(resnum)-1]
    lat = float(res['lat'])
    lon = float(res['lon'])
    isinside = lat >= float(latmin) and lat <= float(latmax) and lon >= float(lonmin) and lon <= float(lonmax)
    assert isinside, "Coordinates (%f,%f) outside bounding box." % (lat, lon)

@step('Then result (\d+) is of type (\w+)')
def run_and_validate_osm_type(step, resnum, osmtype):
    validate_result_number(step, 'at least', resnum)
    validate_osm_type(step, resnum, osmtype)

@step('And then result (\d+) is of type (\w+)')
def validate_osm_type(step, resnum, osmtype):
    assert osmtype == world.results[int(resnum)-1]['osm_type']

@step('Then result (\d+) contains (.*) "(.*)"')
def validate_search_address(step, resnum, addresstype, addressvalue):
    world.params['addressdetails'] = '1'
    validate_result_number(step, 'at least', resnum)
    res = world.results[int(resnum)-1]
    assert addresstype in res['address'], "Expected address to contain '%s'. Got %s." % (addresstype, world.results['address'])
    assert res['address'][addresstype] == addressvalue, "Expected address '%s' to be '%s'. Got %s." % (addresstype, addressvalue, world.results['address'][addresstype])


@step(u'Then a second search excludes previous results')
def validate_excluded_places(step):
    validate_result_number(step, 'at least', 1)
    oldplaceset = set([a['place_id'] for a in world.results])
    world.params['exclude_place_ids'] = ','.join(oldplaceset)
    validate_result_number(step, 'at least', 1)
    for place in world.results:
        assert place['place_id'] not in oldplaceset, "Place %s appeared in both searches" % place['place_id']

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


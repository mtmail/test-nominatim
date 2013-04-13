from nose.tools import *
import urllib
import urllib2
import urlparse
from lettuce import *
from tidylib import tidy_document
import json
from xml.dom.minidom import parseString


@step('a HTTP (\d+) is returned')
def send_and_check_for_error_code(step, http_code='200'):
    data = urllib.urlencode(world.params)
    req = urllib2.Request(url="%s/%s?%s" % (world.base_url, world.requesttype, data),
                          headers=world.header)
    if http_code == '200':
        fd = urllib2.urlopen(req)
        page = fd.read()
    else:
        with assert_raises_regexp(urllib2.HTTPError, http_code):
            urllib2.urlopen(req)

###### XML format in general ################################

@step('xml header does not contain attribute (\w+)')
def check_xml_header_has_not_attribute(step, attr):
    assert_false(world.result.hasAttribute(attr))

@step('xml header contains attribute (\w+) as "(.*)"')
def check_xml_header_has_attribute(step, attr, value):
    assert_true(world.results.hasAttribute(attr))
    assert_true(world.results.getAttribute(attr), value)

@step('xml more url consists of')
def check_xml_more_url_contains(step):
    assert_true(world.results.hasAttribute('more_url'))
    moreurl = urlparse.urlparse(world.results.getAttribute('more_url'))
    params = urlparse.parse_qs(moreurl.query)
    for line in step.hashes:
        assert_true(line['param'] in params, "Missing parameter %s" % line['param'])
        paramvals = params[line['param']]
        assert_equal(len(paramvals), 1)
        assert_equal(paramvals[0], line['value'])
        del params[line['param']]
    assert_false(params)

@step(r'xml contains a viewbox of ([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+)')
def check_xml_viewbox(step, *attr):
    assert_true(world.results.hasAttribute('viewbox'))
    parts = world.results.getAttribute('viewbox').split(',')
    assert_equal(len(parts), 4)
    for i in range(4):
        assert_almost_equal(float(parts[i]), float(attr[i]))


    

############### OLD STUFF ###############################################

@step('Then valid (\w*) is returned')
def validate_format(step, fmt):
    world.call()


########### For search only #################

@step('Then (.+) (\d+) results? is returned')
def validate_result_number(step, operator, number):
    number = int(number)
    world.params['format'] = 'json'
    world.call()
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

@step('Then result (\d+) contains "(.*)"')
def run_validate_display_name_contains(step, resnum, result):
    validate_result_number(step, 'at least', resnum)
    validate_display_name_contains(step, resnum, result)

@step('And then result (\d+) contains "(.*)"')
def validate_display_name_contains(step, resnum, result):
    res = world.results[int(resnum)-1]
    assert res['display_name'].find(result) >= 0, "Expected result to contain '%s', got '%s'." % (result, res['display_name'])

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
    assert addresstype in res['address'], "Expected address to contain '%s'. Got %s." % (addresstype, res['address'])
    assert res['address'][addresstype] == addressvalue, "Expected address '%s' to be '%s'. Got %s." % (addresstype, addressvalue, res['address'][addresstype])


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
    world.call()
    assert 'address' in world.results

@step('Then the address contains (.*) "(.*)"')
def validate_reverse_address(step, addresstype, addressvalue):
    validate_reverse_hasresult(step)
    assert addresstype in world.results['address'], "Expected address to contain '%s'. Got %s." % (addresstype, world.results['address'])
    assert world.results['address'][addresstype] == addressvalue, "Expected address '%s' to be '%s'. Got %s." % (addresstype, addressvalue, world.results['address'][addresstype])


from nose.tools import *
from lettuce import *
import urllib
import urllib2
from lettuce import *
from tidylib import tidy_document
from collections import OrderedDict
import json
from xml.dom.minidom import parseString

@before.each_scenario
def setup_request(feature):
    world.params = {}
    world.header = {}
    world.results = None


@world.absorb
def call():
    if world.results:
        return

    data = urllib.urlencode(world.params)
    req = urllib2.Request(url="%s/%s?%s" % (world.base_url, world.requesttype, data),
                          headers=world.header)
    fd = urllib2.urlopen(req)
    page = fd.read()

    fmt = world.params.get('format')
    if fmt not in ('html', 'xml', 'json', 'jsonv2'):
        fmt = 'xml' if world.requesttype == 'reverse' else 'html'
    pageinfo = fd.info()
    assert_equal('utf-8', pageinfo.getparam('charset').lower())
    pagetype = pageinfo.gettype()
    if fmt == 'html':
        assert_equals('text/html', pagetype)
        document, errors = tidy_document(page, 
                             options={'char-encoding' : 'utf8'})
        assert(len(errors) == 0), "Errors found in HTML document:\n%s" % errors
        world.results = document
    elif fmt == 'xml':
        assert_equals('text/xml', pagetype)
        world.results = parseString(page).documentElement
    else:
        if 'json_callback' in world.params:
            func = world.params['json_callback']
            assert page.startswith(func + '(')
            assert page.endswith(')')
            page = page[(len(func)+1):-1]
            assert_equals('application/javascript', pagetype)
        else:
            assert_equals('application/json', pagetype)
        world.results = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(page)



# possible actions

@step('searching for "(.*)"')
def setup_call_search(step, query):
    world.requesttype = 'search'
    world.params = {}
    world.params['q'] = query.encode('utf8')

@step('looking up coordinates ([-\d.]+),([-\d.]+)')
def setup_call_reverse(step, lat, lon):
    world.requesttype = 'reverse'
    world.params = {}
    world.params['lat'] = lat
    world.params['lon'] = lon 

@step('looking up place (\d+)')
def setup_call_details_place_id(step, placeid):
    world.requesttype = 'details'
    world.params = {}
    world.params['place_id'] = placeid 

@step('looking up osm ([a-z]+) (\d+)')
def setup_call_details_place_id(step, osmtype, osmid):
    world.requesttype = 'details'
    world.params = {}
    world.params['osmtype'] = osmtype
    world.params['osmid'] = osmid 


## Parameter setup

@step('format (\S*)')
def set_format(step, formatstring):
    world.params['format'] = formatstring
    world.results = None

@step('parameter ([\w-]+) as "([^"]*)"')
def set_general_parameter(step, param, value):
    world.params[param] = value
    world.results = None

########## OLD STEPS

@step('With parameters "(.*)"')
def add_parameters(step, paramstring):
    for substr in paramstring.split('&'):
        key, val = substr.split('=')
        world.params[key.encode('utf8')] = val.encode('utf8')
    world.results = None

@step('Using format (\S*)')
def set_format(step, formatstring):
    world.params['format'] = formatstring
    world.results = None

@step('Using language "(.*)"')
def set_language(step, lang):
    world.params['accept-language'] = lang
    world.results = None

@step('Using language header "(.*)"')
def set_language_header(step, lang):
    world.header['Accept-Language'] = lang
    world.results = None

@step('Setting HTTP header "(.*)" to "(.*)"')
def set_http_header(step, header, value):
    world.header[header] = value 
    world.results = None

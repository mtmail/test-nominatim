from lettuce import *

@step('When searching for "(.*)"')
def setup_call_search(step, query):
    world.requesttype = 'search'
    world.params = {'q' : query.encode('utf8') }

@step('When looking up coordinates ([-\d.]+),([-\d.]+)')
def setup_call_reverse(step, lat, lon):
    world.requesttype = 'reverse'
    world.params = {'lat' : lat, 'lon' : lon } 

@step('When looking up place (\d+)')
def setup_call_details_place_id(step, placeid):
    world.requesttype = 'details'
    world.params = { 'place_id' : placeid } 

@step('When looking up osm ([a-z]+) (\d+)')
def setup_call_details_place_id(step, osmtype, osmid):
    world.requesttype = 'details'
    world.params = { 'osmtype' : osmtype, 'osmid' : osmid } 

@step('With parameters "(.*)"')
def add_parameters(step, paramstring):
    for substr in paramstring.split('&'):
        key, val = substr.split('=')
        world.params[key.encode('utf8')] = val.encode('utf8')

@step('Using format (\S*)')
def set_format(step, formatstring):
    world.params['format'] = formatstring

@step('Using language "(.*)"')
def set_language(step, lang):
    world.params['accept-language'] = lang


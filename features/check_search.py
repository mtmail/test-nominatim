from lettuce import *
from nose.tools import *


@step('valid search xml is returned')
def search_validate_xml(step):
    world.call()
    assert world.results.nodeName == "searchresults", \
            "Unexpected element '%s'" % world.results.nodeName
    assert world.results.hasAttribute('attribution')
    assert world.results.hasAttribute('timestamp')
    assert world.results.hasAttribute('querystring')
    assert world.results.hasAttribute('more_url')


@step('valid search json is returned')
def search_validate_json(step):
    world.call()
    assert isinstance(world.results, list), "Result is not a list, it is %s" % type(world.results)


@step('(less than|more than|exactly|at least|at most) (\d+) results? (?:is|are) returned')
def validate_result_number(step, operator, number):
    world.params['format'] = 'json'
    step.given('valid search json is returned')
    number = int(number)
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
        raise Exception("unknown operator '%s'" % operator)

    assert comp, "Bad number of results: expected %s %d, got %d." % (operator, number, numres)


@step('there are( no)? duplicates')
def search_check_for_duplicates(step, nodups=None):
    step.given('at least 1 result is returned')
    resarr = []
    for res in world.results:
        resarr.append((res['osm_type'], res['class'], 
                        res['type'], res['display_name']))

    if nodups is None:
        assert len(resarr) > len(set(resarr))
    else:
        assert_equal(len(resarr), len(set(resarr)))


@step('result (\d+) has attributes (\S+)')
def search_check_for_result_attribute(step, num, attrs):
    step.given('at least %s results are returned' % num)
    res = world.results[int(num)-1]
    for attr in attrs.split(','):
        assert attr in res, "Attribute %s missing" % attr


@step('result (\d+) has attribute (\S+) as "(.*)"')
def search_check_for_result_attribute(step, num, attr, value):
    step.given('at least %s results are returned' % num)
    res = world.results[int(num)-1]
    assert attr in res
    assert_equals(res[attr], value)


@step('result (\d+) is in "(.*)"')
def search_check_for_result_isin(step, num, location):
    step.given('at least %s results are returned' % num)
    res = world.results[int(num)-1]
    addressparts = [ x.strip() for x in res['display_name'].split(',') ]
    assert location in addressparts, "Unexpected address '%s'" % res['display_name']

@step('name of result (\d+) contains "(.*)"')
def search_check_for_result_isin(step, num, name):
    step.given('at least %s results are returned' % num)
    res = world.results[int(num)-1]
    namepart = res['display_name'].split(',', 1)[0].lower()
    assert name.lower() in namepart, "Unexpected address '%s'" % res['display_name']

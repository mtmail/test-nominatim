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
    for node in world.results.childNodes:
        if node.nodeType == 1:
            assert_equals("place", node.nodeName)

@step('valid search json is returned')
def search_validate_json(step):
    world.call()
    assert isinstance(world.results, list), "Result is not a list, it is %s" % type(world.results)

def compare(operator, op1, op2):
    if operator == 'less than':
        return op1 < op2
    elif operator == 'more than':
        return op1 > op2
    elif operator == 'exactly':
        return op1 == op2
    elif operator == 'at least':
        return op1 >= op2
    elif operator == 'at most':
        return op1 <= op2
    else:
        raise Exception("unknown operator '%s'" % operator)

@step('(less than|more than|exactly|at least|at most) (\d+) results? (?:is|are) returned')
def validate_result_number(step, operator, number):
    world.params['format'] = 'json'
    step.given('valid search json is returned')
    number = int(number)
    numres = len(world.results)
    assert compare(operator, numres, number), \
        "Bad number of results: expected %s %d, got %d." % (operator, number, numres)

@step('(less than|more than|exactly|at least|at most) (\d+) xml results? (?:is|are) returned')
def validate_result_number(step, operator, number):
    world.params['format'] = 'xml'
    step.given('valid search xml is returned')
    number = int(number)
    numres = len(world.results.getElementsByTagName('place'))
    assert compare(operator, numres, number), \
        "Bad number of results: expected %s %d, got %d." % (operator, number, numres)



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

@step('result (\d+) has not attributes (\S+)')
def search_check_for_result_attribute(step, num, attrs):
    step.given('at least %s results are returned' % num)
    res = world.results[int(num)-1]
    for attr in attrs.split(','):
        assert attr not in res, "Unexpected attribute '%s'" % attr


@step('xml result (\d+) has attributes (\S+)')
def search_xml_check_for_result_attribute(step, num, attrs):
    step.given('at least %s xml results are returned' % num)
    res = world.results.getElementsByTagName('place')[int(num)-1]
    for attr in attrs.split(','):
        assert res.hasAttribute(attr), "Attribute %s missing" % attr

@step('xml result (\d+) has not attributes (\S+)')
def search_xml_check_for_result_attribute(step, num, attrs):
    step.given('at least %s xml results are returned' % num)
    res = world.results.getElementsByTagName('place')[int(num)-1]
    for attr in attrs.split(','):
        assert res.hasAttribute(attr), "Unexpected attribute '%s'" % attr



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

@step('result (\d+) has address details with "(.*)"')
def search_check_for_address_details(step, num, name):
    step.given('at least %s results are returned' % num)
    res = world.results[int(num)-1]
    assert 'address' in res
    assert name in res['address'].values()

@step('result (\d+) has address details in order ([\w,]+)')
def search_check_address_detail_order(step, num, partstr):
    step.given('at least %s results are returned' % num)
    res = world.results[int(num)-1]
    parts = [ x.strip() for x in partstr.split(',')]
    assert 'address' in res
    assert_equals(parts, res['address'].keys())

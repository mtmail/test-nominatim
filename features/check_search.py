from lettuce import *


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


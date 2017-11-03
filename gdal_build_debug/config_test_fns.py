# -*- coding: utf-8 -*-
"""
Functions supporting testing of the config log
"""

import re
import click
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
# ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def check_result(data):
    """
    Returns a boolean whether the test passed or encountered fatal failures.
    Args:
        data: a list of tuples of the form (
            int line number,
            (str|NoneType test result, (int start, end of test to highlight)),
            str full line,
            bool is failing the test on this line fatal
        )
    """
    essential_success = True
    non_essential_success = False
    essential_lines_present = False
    for _, (result, _), _, essential in data:
        if essential:
            essential_success = essential_success and result != 'failure'
            if not essential_lines_present:
                essential_lines_present = True
    if essential_lines_present:
        return essential_success
    else:
        return non_essential_success


def style_result(data):
    """
    echoes lines related to a test result with ANSI colors
    Args:
        data: (
            int line number,
            (str|NoneType test_satisfaction, (int start, int end)),
            str line,
            bool essential
            )
    """
    line_num, (test_result, indexes), line, essential = data
    final = ''
    color = 'light grey'
    start = 0
    end = len(line)
    if test_result[0] == 'passes':
        start, end = indexes
        color = 'green'
    elif test_result[0] == 'failure':
        start, end = indexes
        color = 'red'
    else:
        color = 'white'
    final = '{}\t{}{}{}'.format(
        line_num,
        click.style(line[0:start], fg='white'),
        click.style(line[start:end], fg=color),
        click.style(line[end:len(line)], fg='white')
    )
    click.echo(final)


def style_results(results):
    """
    Echoes styled results to the command line and returns a boolean, whether
    all tests passed.
    Args:
        results: a dict mapping search name to a list of tuples representing
            tested lines
    Returns:
        a boolean, whether all tests passed
    """
    all_clear = True
    for result in sorted(results.items(), key=lambda item: item[0].lower()):
        key, data = result
        if check_result(data) and len(data) > 0:
            click.echo(
                '{}:\t\t{}'.format(
                    key,
                    click.style('✓', fg='green')
                )
            )
        else:
            all_clear = False
            click.echo(
                '{}:\t\t{}'.format(
                    key,
                    click.style('×', fg='red')
                )
            )
            for line in data:
                style_result(line)
        return all_clear


def get_group(match, *names):
    """
    Returns the first resolved regex match group from the given identifiers
    Args:
        match: a re.match object
        names: multiple int or str group indexes/names, in the order they
            should be tried
    Returns:
        a tuple of the start and end indexes of the match group
    """
    for name in names:
        try:
            return match.group(name) and (match.start(name), match.end(name))
        except IndexError:
            continue  # try the next name
    else:
        return  # return None if no recognized name present


# unit testing material
# match = re.match('abc: (?P<a>1)', 'abc: 1')
# assert not get_pass(match)
# assert get_success(match)
# assert not get_failure(match)


def get_success(match):
    success = get_group(match, 'success', 1)
    return ('success', success) if success else None


def get_pass(match):
    """
    contains no group index since as an optional value, it must be explicityly
    named
    """
    acceptable = get_group(match, 'pass')
    return ('pass', acceptable) if acceptable else (None, None)


def get_failure(match):
    failure = get_group(match, 'fail', 'failure', 2)
    return ('failure', failure) if failure else None


def default_filter(query, line):
    """Returns a string to test iff the query matches the line"""
    if query in line.lower():
        split = re.split(':(\.\.\.)')
        return split[-1]


def default_test(response, accept_internal=True):
    "Returns a test response tuple based on a given response string"
    def answer(satisfies_test):
        return (satisfies_test, (response, 0, len(response)))
    if 'no' not in response:
        if any([a in response for a in ['yes', 'enabled']]):
            return answer('success')
        elif accept_internal:
            return answer('success')
        else:
            return answer('failure')
    else:
        return ('failure', (response, 0, len(response)))


def regex_filter(query, line):
    "returns a regex match or None"
    return query.search(line)


def regex_test(query, to_test):
    match = query.search(to_test) if type(to_test) is str else to_test
    return get_success(match) or get_failure(match) or get_pass(match)

# unit testing material:
# def check_response(resp_obj):
#  assert type(resp_obj) is tuple;
#  assert len(resp_obj) == 4
#  line_num, test_resp, line, is_essential = resp_obj
#  assert type(line_num) is int
#  assert type(test_success) is str or test_success is None
#  test_success, (start, end) = test_resp
#  assert start is None or type(start) is int
#  assert end is None or type(end) is int
#  assert type(line) is str
#  assert type(is_essential) is bool


def is_regex_str(query):
    'a naive check of whether a str is intended to be regex'
    return any([i in query for i in '[()]\\'])


def make_test(query, accept_internal=True):
    """
    Returns a test function of whether a passed line succeeded or not
    """
    query = query.partition(':::')
    query = query[2] or query[0]
    if is_regex_str(query):
        regex = re.compile(query)

        def test(line):
            return regex_test(regex, line)
    else:
        def test(line):
            return default_test(re.compile(query), line, accept_internal)
    return test


def make_search(query):
    'returns a filter function based on a query'
    if type(query) is not str:
        raise ValueError('query is not a string')
    # the search for matching lines
    query = query.split(':::')[0]
    if is_regex_str(query):
        regex = re.complile(query, flags=re.I)

        def search(line):
            return regex_filter(regex, line)
    else:
        def search(line):
            return default_filter(query, line)
    return search


def check_lines(filter_fn, test_fn, config_log_lines, essential=False):
    """"
    Pipes all lines through the filter_ and test_fns, returns the resulting
    list of tuples
    """
    results = []
    for index, line in enumerate(config_log_lines):
        match = filter_fn(line)
        if match:
            results.append(
                (index + 1, test_fn(match), line, essential)
            )
    return results


# def test_config_support(lib, config_results, pass_internal=True):
#    "Returns True iff the final configuration results all pass the input test"
#     search = re.compile(r'(?ims){}[^:]*:\W*(?P<response>\w+)'.format(lib))
#     matches = re.findall(search, config_results)
#     if pass_internal:
#         def test(r): 'no' not in r
#     else:
#         def test(r): r == 'yes'
#     return all(map(test, matches))


def main(config_log, queries, accept_internal=True):
    """
    Given a string config_log, and an iterable of queries (either supported
    libraries or custom searches), runs the full 'test suite'
    """
    checks, _, support = config_log.partition('GDAL is now configured')
    checks_lines, support_lines = checks.split('\n'), support.split('\n')
    results = {}
    for query in queries:
        search_fn, test_fn = make_search(query), make_test(query)
        results[query] = check_lines(search_fn, test_fn, support_lines, True)
        results[query] = check_lines(search_fn, test_fn, checks_lines, False)
    return style_results(results)

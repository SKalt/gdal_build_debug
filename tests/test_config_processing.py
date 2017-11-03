from gdal_build_debug.config_test_fns import \
    style_results, get_pass, get_success, get_failure, \
    regex_test, default_test, default_filter, check_result, \
    main, make_test
from .fixtures.line_endings_that_should_fail import \
    line_endings_that_should_fail
from .fixtures.line_endings_that_should_pass import \
    line_endings_that_should_pass
import pytest
import re
import os

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


def test_style_results():
    results = {'foo': [(1, ('success', (0, 1)), 'bar', True)]}
    assert style_results(results)
    results = {'foo': [(1, ('failure', (0, 1)), 'bar', True)]}
    assert not style_results(results)
    # results = {'foo': [(1, ('failure', (0, 1)), 'bar', False)]}
    # assert not style_results(results)
    # results = {'foo': [(1, ('success', (0, 1)), 'bar', False)]}
    # assert style_results(results)
    # results = {'foo': [(1, ('pass', (0, 1)), 'bar', False)]}
    # assert style_results(results)
    # results = {'foo': [(1, (None, None), 'bar', False)]}
    # assert style_results(results)
    # results = {'foo': [(1, (None, None), 'bar', True)]}
    # assert style_results(results)


def test_get_group():
    match = re.match('abc:\s*(1)', 'abc: 1')
    assert get_pass(match) == (None, None)
    assert get_success(match)
    assert not get_failure(match)
    match = re.match('abc: (foo)?(?P<success>1)', 'abc: 1')
    assert get_pass(match) == (None, None)
    assert get_success(match)
    assert get_failure(match) # faiure looks at group 2
    assert regex_test('pass', match)
    assert regex_test('pass', match)[0] == 'success'
    match = re.match('abc: (foo)?(?P<failure>1)', 'abc: 1')
    assert get_pass(match) == (None, None)
    assert not get_success(match)
    assert get_failure(match)


def test_check_results():
    data = [(1, ('success', (0, 1)), 'bar', True)]
    assert check_result(data)
    data = [
        (1, ('success', (0, 1)), 'bar', True),
        (2, ('success', (1, 2)), 'bar', True)
    ]
    assert check_result(data)
    data = [
        (1, ('success', (0, 1)), 'bar', True),
        (2, ('failure', (1, 2)), 'bar', True)
    ]
    assert not check_result(data)
    data = [
        (1, ('success', (0, 1)), 'bar', True),
        (2, ('failure', (1, 2)), 'bar', True)
    ]
    assert not check_result(data)
    data = [
        (1, ('success', (0, 1)), 'bar', True),
        (2, ('failure', (1, 2)), 'bar', False)
    ]
    assert check_result(data)
    assert check_result(data[::-1])
    
# def test_response():
#     resp_obj = # the output of a test fn
#     assert type(resp_obj) is tuple
#     assert len(resp_obj) == 4
#     line_num, test_resp, line, is_essential = resp_obj
#     assert type(line_num) is int
#     assert type(check_success) is str or check_success is None
#     check_success, (start, end) = test_resp
#     assert start is None or type(start) is int
#     assert end is None or type(end) is int
#     assert type(line) is str
#     assert type(is_essential) is bool

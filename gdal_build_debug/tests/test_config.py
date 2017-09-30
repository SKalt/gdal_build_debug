import re
import os
import pytest
from ..gdal_build_debug import search_config_log as search_config_log


@pytest.fixture(scope='module')  # deprecated -> redundant
def supported_libs():
    __location__ = os.path.realpath(
        os.path.join(
            os.getcwd(),
            os.path.dirname(__file__)
        )
    )
    with open(os.path.join(__location__, '..', 'supported.txt')) as supported:
        return set(
            filter(
                lambda x: x,
                map(
                    lambda x: x.lower().strip(),
                    supported.read().split('\n')
                )
            )
        )

# def test_args(config_log, support, supported_libs, informative):
#     print(config_log and True, support, supported_libs, informative)
#     assert 0

def raise_informative_error(config_log, support, *mo_re):
    informative_error = search_config_log(config_log, support, *mo_re)
    raise ValueError(informative_error)


@pytest.mark.test_dependencies
def test_supported(config_log, support, supported_libs, informative):
    """
    Given a lib name and a config log, check if the config succeeded. Else,
    output lines relevant to the lib
    """
    if support not in supported_libs:
        print(support + 'is not among testable support libraries')
        return
    regex_test = r'(?ims){}.*support:\W*(?P<response>\w+)'.format(support)
    matches = re.findall(regex_test, config_log)
    try:
        assert all(map(lambda x: x in ['yes', 'internal'], matches))
        assert matches
    except AssertionError:
        print('no {} support'.format(support))
        if informative:
            raise_informative_error(config_log, support)
        else:
            raise AssertionError('no {} support'.format(support))


@pytest.mark.test_dependencies
def test_not_supported(config_log, no_support, supported_libs, informative):
    if no_support not in supported_libs:
        print(no_support + 'is not among testable support libraries')
        return
    regex_test = r'(?ims){}.*support:\W*(?P<response>\w+)'.format(no_support)
    matches = re.findall(regex_test, config_log)
    try:
        assert all(map(lambda x: x not in ['yes', 'internal'], matches))
        assert matches
    except AssertionError:
        print('unexpected {} support'.format(no_support))
        if informative:
            raise_informative_error(config_log, no_support)
        else:
            raise AssertionError('unexpected {} support'.format(no_support))

import re
import os
import pytest


@pytest.fixture(scope='module')
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


def raise_informative_error(config_log, support, *mo_re):
    regex = '|'.join([r'({})'.format(i) for i in [support] + list(mo_re)])
    informative_error = ''
    for num, line in enumerate(config_log.split('\n')):
        if regex.match(line):
            informative_error += '{}\t{}\n'.format(num + 1, line)


@pytest.mark.test_config
def test_supported(config_log, included, supported_libs, informative):
    """
    Given a lib name and a config log, check if the config succeeded. Else,
    output lines relevant to the lib
    """
    if included not in supported_libs:
        print(included + 'is not among testable support libraries')
        return
    regex_test = r'(?ims){}.*support:\W*(?P<response>\w+)'.format(included)
    matches = re.findall(regex_test, config_log)
    try:
        assert all(map(lambda x: x in ['yes', 'internal'], matches))
        assert matches
    except AssertionError:
        print('no {} support'.format(included))
        if informative:
            raise_informative_error(config_log, included)
        else:
            raise AssertionError('no {} support'.format(included))

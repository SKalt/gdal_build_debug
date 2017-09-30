# -*- coding: utf-8 -*-
'Functions supporting testing of the config log'

import re

_regex = re.compile(r'(?is)(yes|enabled)\W+$')


def check_support_line(num, line, support_lib, regex, mode='string'):
    """
    Checks a line for support of `support_lib` and returns a string, tuple, or
    AssertionError with all relevant info.
    """
    if regex.match(line):
        num += 1
        is_supported = bool(re.match(_regex, line))
        if mode == 'tuple':
            return (support_lib, is_supported, num, line)
        elif mode == 'string':
            return '{}\t{}\n'.format(num, line)
        elif mode == 'err':
            msg = '{} not supported : {}\t{}'.format(support_lib, num, line)
            return AssertionError(msg)


def search_config(config_log, support, *mo_re):
    """
    Returns all lines & numbers matching the named support or additional regex
    tests
    """
    regex = re.compile(
        pattern='|'.join([r'({})'.format(i) for i in [support] + list(mo_re)])
    )
    lines = ''
    for num, line in enumerate(config_log.split('\n')):
        if regex.match(line):
            lines += '{}\t{}\n'.format(num + 1, line)
    return lines

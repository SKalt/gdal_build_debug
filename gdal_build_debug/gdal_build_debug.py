# -*- coding: utf-8 -*-

"""Main module."""

import re


# regex to parse args
flag_parse_regex = re.compile(r'--with(out)?-([\w-]+)(=(\w+))?')


def parse_flag(flag):
    "parse a config argument"
    match = re.match(flag_parse_regex, flag)
    if not match:
        return False
    else:
        return match.groups()

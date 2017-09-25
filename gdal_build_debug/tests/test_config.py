import re


def test_lib_included_in_config(config_log, included_lib, internal=True,
                                *more_re
                                ):
    """
    Given a lib name and a config log, check if the config succeeded. Else,
    output lines relevant to the lib
    """
    # open log, read log as log
    lib = included_lib
    regex_test = r'(?ims)\W*{} support:\W*(?P<response>\w+)'.format(lib)
    matches = re.findall(regex_test, config_log)
    assert matches
    try:
        assert all(map(lambda x: x in ['yes', 'internal'], matches))
    except AssertionError:
        more_re = [included_lib] + more_re
        tests = map(lambda x: '^.*({}).*\.{3}.*$'.format(x), more_re)
        new_regex_test = r'(?im)({})'.format('|'.join(tests))
        informative_error = ''
        for num, line in config_log.split('\n'):
            if new_regex_test.match(line):
                informative_error += '{}\t{}\n'.format(num + 1, line)
        print(informative_error)
        raise AssertionError(included_lib + ' not included')

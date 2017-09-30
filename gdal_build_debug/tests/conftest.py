import pytest
# import re


# def pytest_cmdline_preparse(args):
#     ''
#     regex = re.compile(r'--(?P<inclusion>with(out)?)-(?P<lib>\S+)')
#     other = []
#     inclusion = []
#     for arg in args:
#         match = regex.match(arg)
#         if match:
#             inclusion.append('--{}={}'.format(
#                     match.group('inclusion'),
#                     match.group('lib')
#                 )
#             )
#         else:
#             other.append(arg)
#     args = other + inclusion


def pytest_addoption(parser):
    """
    Add command-line options for Pytest to parse.
    """
    parser.addoption(
        '--with', action='append', default=[],
        help='libs to test are included'  # TODO: eloquence
    )
    parser.addoption(
        '--without', action='append', default=[],
        help='libs to test are excluded'
    )
    parser.addoption(
        '--supported', action='append', default=[],
        help='dependencies to test are met'
    )
    parser.addoption(
        '--not-enabled', action='append', default=[],
        help='libs to test are excluded'
    )
    parser.addoption(
        '--path-to-config-log', action='store', default='./configure.log',
        help='path to configuration logs'
    )
    parser.addoption(
        '--test-version-is', action='store_true',
        default=False, help='includes test that command-line gdal version' +
        ' is equal to input'
    )
    parser.addoption(
        '--informative', action='store_true',
        default=False, help='Whether to output lines detailing support in' +
        'errors'
    )
    # parser.addoption(
    #     '--test-path', action='store_true', default=False,
    #     help='includes a test of that the command-line gdal version' +
    #     ' is equal to input'
    # )
    parser.addoption(
        '--test-dependencies', action='store_true', default=False,
        help='include tests on your config log'
    )
    parser.addoption(
        '--test-formats', action='store_true', default=False,
        help='include tests on the gdal/ogrinfo reacheable from the command' +
        'line'
    )
    # parser.addoption(
    #     '--mode', action='store', default='gdal', help='ogr or gdal'
    # )


def pytest_generate_tests(metafunc):
    if 'included' in metafunc.fixturenames:
        included = list(set(metafunc.config.getoption('with')))
        metafunc.parametrize('included', included, scope='session')
    if 'excluded_lib' in metafunc.fixturenames:
        excluded_libs = list(set(metafunc.config.option.without))
        metafunc.parametrize('excluded_lib', excluded_libs, scope='session')


def pytest_collection_modifyitems(config, items):
    "skip non-requested sub-suites of tests"
    for _test in ['version-is', 'formats', 'dependencies']:
        _test_value = config.getoption('--test-' + _test)
        if not _test_value:
            skip = pytest.mark.skip(
                reason='needs --test-{} to run'.format(_test)
            )
            for item in items:
                if 'test_' + _test.replace('-', '_') in item.keywords:
                    item.add_marker(skip)

@pytest.fixture
def informative(request):
    return True if request.config.getoption('--informative') else False


@pytest.fixture
def config_log(request):
    """
    Where you put your log from `gdal-src/configure [options] > config.log`
    """
    conf_log_path = request.config.getoption('--path-to-config-log')
    with open(conf_log_path) as conf_log_file:
        return conf_log_file.read()

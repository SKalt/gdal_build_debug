import pytest
import re


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
    parser.addoption(
        '--with', action='append', default=[],
        help='libs to test are included'  # TODO: eloquence
    )
    parser.addoption(
        '--without', action='append', default=[],
        help='libs to test are excluded'
    )
    parser.addoption(
        '--conf-log', action='store', default='.',
        help='path to directory with logs'
    )
    parser.addoption(
        '--test-version', action='store_true',
        default=False, help='includes test that command-line gdal version' +
        ' is equal to input'
    )
    parser.addoption(
        '--test-path', action='store_true', default=False,
        help='includes a test of that the command-line gdal version' +
        ' is equal to input'
    )
    parser.addoption(
        '--test-config', action='store_true', default=True,
        help='include tests on your config log'
    )
    parser.addoption(
        '--test-cli', action='store_true', default=False,
        help='include tests on the gdal/ogrinfo reacheable from the command' +
        'line'
    )
    # parser.addoption(
    #     '--mode', action='store', default='gdal', help='ogr or gdal'
    # )


def pytest_generate_tests(metafunc):
    if 'included_lib' in metafunc.fixturenames:
        included_libs = list(set(metafunc.config.getoption('with')))
        metafunc.parametrize('included_lib', included_libs, scope='session')
    if 'excluded_lib' in metafunc.fixturenames:
        excluded_libs = list(set(metafunc.config.option.without))
        metafunc.parametrize('excluded_lib', excluded_libs, scope='session')


def pytest_collection_modifyitems(config, items):
    for _test in ['version', 'path', 'cli']:
        _test_value = config.getoption('--test-' + _test)
        if not _test_value:
            skip = pytest.mark.skip(
                reason='needs --test-{} to run'.format(_test)
            )
            for item in items:
                if 'test_' + _test in item.keywords:
                    item.add_marker(skip)

@pytest.fixture
def config_log_file(conf_log_path):
    """
    Where you put your log from `gdal-src/configure [options] > config.log`
    """
    with open(conf_log_path) as conf_log_file:
        return conf_log_file.read().split('\n')

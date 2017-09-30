import os
import pytest
import pandas as pd

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)
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
        '--with-gdal-format', action='append', default=[],
        help='libs to test are included'  # TODO: eloquence
    )
    parser.addoption(
        '--with-ogr-format', action='append', default=[],
        help='libs to test are included'  # TODO: eloquence
    )
    parser.addoption(
        '--without-gdal-format', action='append', default=[],
        help='libs to test are included'  # TODO: eloquence
    )
    parser.addoption(
        '--without-ogr-format', action='append', default=[],
        help='libs to test are included'  # TODO: eloquence
    )
    parser.addoption(
        '--with-dependency', action='append', default=[],
        help='dependencies to test are met'
    )
    parser.addoption(
        '--without-dependency', action='append', default=[],
        help='libs to test are excluded'
    )
    parser.addoption(
        '--path-to-config-log', action='store', default='./configure.log',
        help='path to configuration logs'
    )
    parser.addoption(
        '--test-version-is', action='store',
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
    def included(fixture):
        return fixture in metafunc.fixturenames

    def include(fixture, name):
        if included(fixture):
            metafunc.parametrize(fixture, metafunc.config.getoption(name))
    #print(metafunc.config.option)
    #include('version_is', 'test_version_is')
    include('gdal_format', 'with_gdal_format')
    include('gdal_format_excluded', 'without_gdal_format')
    include('ogr_format', 'with_ogr_format')
    include('ogr_format_excluded', 'without_gdal_format')
    include('support', 'with_dependency')
    include('no_support', 'without_dependency')


def pytest_collection_modifyitems(config, items):
    "skip non-requested sub-suites of tests"
    #print(dir(config), '\n\n', dir(items), '\n\n', items)
    for _test in ['version-is', 'formats', 'dependencies']:
        _test_value = config.getoption('--test-' + _test)
        #print(_test, _test_value)
        if not _test_value:
            skip = pytest.mark.skip(
                reason='needs --test-{} to run'.format(_test)
            )
            for item in items:
                #print(item, [i for i in item.keywords.items()])
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

@pytest.fixture
def version_is(request):
    return request.config.getoption('--test-version-is')

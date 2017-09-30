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
    print(metafunc.fixturenames)

    def sort_formats(cli):
        'Sort arguments by their belonging to ogr and/or GDAL'
        for include in [True, False]:
            fixture_name = cli + '_format' + ('' if include else '_excluded')
            if fixture_name in metafunc.fixturenames:
                inclusion = 'with' + ('' if include else 'out')
                __cluded_formats = set(metafunc.config.getoption(inclusion))
                cli_formats = set(
                    pd.read_csv(
                        os.path.join(
                            __location__, '..', cli + '_formats.csv'
                        )
                    )['Code'].apply(lambda code: code.lower().strip())
                )
                formats = list(__cluded_formats.intersection(cli_formats))
                metafunc.parametrize(fixture_name, formats, scope='session')

    _support = ('support', 'no_support')
    # print(metafunc.fixturenames)
    # if any(map(lambda x: x in metafunc.fixturenames, _support)):
    assert metafunc.config.getoption('--test-dependencies')
    with open(os.path.join(__location__, '..', 'supported.txt')) as f:
        libs = set([i.strip().lower() for i in f.read().split('\n')])
    for included in [True, False]:
        support = ('no_' if included else '') + 'support'
        if support in metafunc.fixturenames:
            included = metafunc.config.getoption(
                'with' + ('' if included else 'out')
            )
            supported = list(libs.intersection(included))
            metafunc.parametrize(support, supported, scope='session')
        else:
            print(metafunc.fixturenames)

    # else:
    #     print(metafunc.fixturenames)
    #     assert 0
    for cli in ['ogr', 'gdal']:
        sort_formats(cli)


def pytest_collection_modifyitems(config, items):
    "skip non-requested sub-suites of tests"
    print(dir(config), '\n\n', dir(items), '\n\n', items)
    for _test in ['version-is', 'formats', 'dependencies']:
        _test_value = config.getoption('--test-' + _test)
        print(_test, _test_value)
        if not _test_value:
            skip = pytest.mark.skip(
                reason='needs --test-{} to run'.format(_test)
            )
            for item in items:
                print(item, [i for i in item.keywords.items()])
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

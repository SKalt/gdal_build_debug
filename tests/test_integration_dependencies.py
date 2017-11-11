l"""
python cli.py --with postgis test --dependencies
python cli.py --with postgis test
python cli.py --with sqlite test --dependencies
python cli.py --with postgis test --config
python cli.py --with postgis test --formats
python cli.py --with=pdf test --formats
python cli.py --with=postgis test --formats
python cli.py  test --with=postgis --formats
python cli.py  test --with=postgis --formats
with:postgis
"""
from .fixtures.line_endings_that_should_fail import \
    line_endings_that_should_fail
from .fixtures.line_endings_that_should_pass import \
    line_endings_that_should_pass
import pytest
import re
import subprocess
import os
os.unsetenv('WITH')
os.unsetenv('WITHOUT')
os.unsetenv('PATH_TO_GDAL_CONFIG_LOG')

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)

config_log_path = __location__ + '/fixtures/configure.log'
os.environ['PATH_TO_GDAL_CONFIG_LOG'] = config_log_path


def call(arg, *args):
    'calls args'
    return subprocess.run(
        [i for i in arg.split()] + [i for i in args],
        check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )

def call_cli(arg, *args):
    args = arg.split() + [i for i in args]
    return call(
        'python',
        os.path.join(__location__, '..', 'gdal_build_debug', 'cli.py'),
        *args
    )


@pytest.mark.parametrize('dep', [  # TODO: add some that pass from regex
    'GRIB', 'PCIDSK', 'QHull', 'LIBGIF', 'LIBJPEG', '12-bit', 'mrf'
    ])
def test_all_expected_inclusions_pass(dep):
    # print(call_cli + ['--with=GEOS'] + options)
    completed = call_cli('--with={} test --dependenies'.format(dep))
    assert '✓' in completed.stdout.decode()


def test_multiple_inclusions_pass():
    completed = call_cli('--with=GEOS --with=grib test --dependencies'),
    assert len(re.findall('✓', completed.stdout.decode())) == 2


def test_single_exclusion_passes(options):
    completed = call_cli('--without=sqlite test --dependencies')
    assert '✓' in completed.stdout.decode()


def test_multiple_exclusions_pass():
    completed = call_cli(
        '--verbose --without=spatialite --without=OpenCL test --dependencies'
    )
    print(completed.stdout.decode())
    assert len(re.findall('✓', completed.stdout.decode())) == 2


def test_multiple_exclusions_fail():
    completed = call_cli(
        '--without=grib --without=geojson test --dependencies'
    )
    raise AssertionError('expected 2 tests to fail')
    assert len(re.findall('×', completed.stdout.decode())) == 2

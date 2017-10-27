import pytest
import subprocess
import os
os.unsetenv('WITH')
os.unsetenv('WITHOUT')
__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


@pytest.fixture(scope='module')
def call_cli():
    return ['python', __location__ + '/../gdal_build_debug/cli.py']


@pytest.fixture(scope='module')
def options():
    return [
        'test',
        '--path-to-config-log=' + __location__ + '/fixtures/configure.log',
        '--dependencies'
    ]


def test_single_inclusion_passes(call_cli, options):
    # print(call_cli + ['--with=GEOS'] + options)
    completed = subprocess.run(
        call_cli + ['--with=GEOS'] + options, stdout=subprocess.PIPE,
        check=True
    )
    assert '1 passed' in completed.stdout.decode()


def test_multiple_inclusions_pass(call_cli, options):
    completed = subprocess.run(
        call_cli + ['--with=GEOS', '--with=grib'] + options,
        stdout=subprocess.PIPE,
        check=True
    )
    print(completed.stdout.decode('utf8'))
    assert '2 passed' in completed.stdout.decode()


def test_single_exclusion_passes(call_cli, options):
    completed = subprocess.run(
        call_cli + ['--without=sqlite'] + options,
        stdout=subprocess.PIPE,
        check=True
    )
    print(completed.stdout.decode('utf8'))
    assert '1 passed' in completed.stdout.decode()


def test_multiple_exclusions_pass(call_cli, options):
    completed = subprocess.run(
        call_cli + ['--without=sqlite', '--without=OpenCL'] + options,
        stdout=subprocess.PIPE,
        check=True
    )
    print(completed.stdout.decode('utf8'))
    assert '2 passed' in completed.stdout.decode()


def test_multiple_exclusions_fail(call_cli, options):
    try:
        completed = subprocess.run(
            call_cli + ['--without=grib', '--without=geojson'] + options,
            stdout=subprocess.PIPE,
            check=True
        )
        print(completed.stdout.decode('utf8'))
        raise AssertionError('expected 2 tests to fail')
    except subprocess.CalledProcessError as err:
        assert err.args[0]

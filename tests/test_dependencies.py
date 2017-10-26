import pytest
import subprocess
import os

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


def test_single_inclusion(call_cli, options):
    # print(call_cli + ['--with=GEOS'] + options)
    completed = subprocess.run(
        call_cli + ['--with=GEOS'] + options, stdout=subprocess.PIPE,
        check=True
    )
    assert '1 passed' in completed.stdout.decode()


def test_multiple_inclusions(call_cli, options):
    completed = subprocess.run(
        call_cli + ['--with=GEOS', '--with=grib'] + options,
        stdout=subprocess.PIPE,
        check=True
    )
    print(completed.stdout.decode('utf8'))
    assert '2 passed' in completed.stdout.decode()

"Tests the GDAL/OGR command-line support for desired formats"
import subprocess
import pytest
import os
import re
import pandas as pd


@pytest.fixture(scope="module")
def lookup():
    class formats(object):
        "Holds gdal/ogr format infomration"
        def __init__(self):
            __location__ = os.path.realpath(
                os.path.join(
                    os.getcwd(),
                    os.path.dirname(__file__)
                )
            )
            self.gdal = pd.read_csv(
                os.path.join(__location__, '..', 'gdal_formats.csv')
            )
            self.ogr = pd.read_csv(
                os.path.join(__location__, '..', 'ogr_formats.csv')
            )
            self.ogr_codes = set(self.ogr['Code'].apply(lambda x: x.lower()))
            self.gdal_codes = set(self.gdal['Code'].apply(lambda x: x.lower()))

        def format(self, fmt):
            "Returns ogr/gdal, depending on which supports the supplied format"
            fmt = fmt.lower()
            if fmt in self.ogr_codes:
                return 'ogr'
            elif fmt in self.gdal_codes:
                return 'gdal'
            else:
                raise AssertionError(fmt + ' is not supported by gdal/ogr')

    return formats()


@pytest.mark.test_cli
def test_format_installed(included, lookup):
    "Checks a foramt is installed"
    mode = lookup.format(included) + 'info'
    subprocess.run([mode, '--format', included], check=True)


@pytest.mark.test_cli
def test_format_excluded(included, lookup):
    "Checks a format is excluded from the buid"
    mode = lookup.format(included) + 'info'
    included = True
    try:
        subprocess.run([mode, '--format', included], check=True)
    except subprocess.CalledProcessError:
        included = False
    if included:
        raise ValueError(included + ' is included')
    else:
        assert True


@pytest.mark.test_cli
@pytest.mark.test_version_is
def test_version_is(version_to_check):
    version_to_check = version_to_check.replace('.', '\.')
    output = subprocess.run(['gdalinfo', '--version'], stdout=subprocess.PIPE)
    assert re.match(version_to_check, output.stdout.decode())

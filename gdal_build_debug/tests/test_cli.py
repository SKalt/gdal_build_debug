"Tests the GDAL/OGR command-line access to desired libraries"
import subprocess
import pytest
import os
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
                os.path.join(__location__, 'gdal_formats.csv')
            )
            self.ogr = pd.read_csv(
                os.path.join(__location__, 'ogr_formats.csv')
            )
            self.ogr_codes = set(self.ogr['Code'].apply(lambda x: x.lower()))
            self.gdal_codes = set(self.gdal['Code'].apply(lambda x: x.lower()))

        def format(self, fmt):
            "Returns ogr/gdal, depending on which supports the supplied format"
            fmt = fmt.lower()
            if fmt in self.ogr_formats:
                return 'ogr'
            elif fmt in self.gdal_formats:
                return 'gdal'
            else:
                raise AssertionError(fmt + ' is not supported by gdal/ogr')

    return formats()


@pytest.mark.test_cli
def test_format_installed(format_to_check, lookup):
    "Checks a foramt is installed"
    mode = lookup.format(format_to_check) + 'info'
    subprocess.run([mode, '--format', format_to_check], check=True)


@pytest.mark.test_cli
def test_format_excluded(format_to_check, lookup):
    "Checks a format is excluded from the buid"
    mode = lookup.format(format_to_check) + 'info'
    included = True
    try:
        subprocess.run([mode, '--format', format_to_check], check=True)
    except subprocess.CalledProcessError:
        included = False
    if included:
        raise ValueError(format_to_check + ' is included')
    else:
        assert True

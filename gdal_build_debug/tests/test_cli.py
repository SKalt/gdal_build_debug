"Tests the GDAL/OGR command-line support for desired formats"
import subprocess
import pytest
import os
import re
import pandas as pd


# @pytest.fixture(scope="module")
# def lookup():
#     class formats(object):
#         "Holds gdal/ogr format infomration"
#         def __init__(self):
#             __location__ = os.path.realpath(
#                 os.path.join(
#                     os.getcwd(),
#                     os.path.dirname(__file__)
#                 )
#             )
#             self.gdal = pd.read_csv(
#                 os.path.join(__location__, '..', 'gdal_formats.csv')
#             )
#             self.ogr = pd.read_csv(
#                 os.path.join(__location__, '..', 'ogr_formats.csv')
#             )
#             self.ogr_codes = set(self.ogr['Code'].apply(lambda x: x.lower()))
#             self.gdal_codes = set(self.gdal['Code'].apply(lambda x: x.lower()))
#
#         def format(self, fmt):
#             "Returns ogr/gdal, depending on which supports the supplied format"
#             fmt = fmt.lower()
#             if fmt in self.ogr_codes:
#                 return 'ogr'
#             elif fmt in self.gdal_codes:
#                 return 'gdal'
#             else:
#                 raise AssertionError(fmt + ' is not supported by gdal/ogr')
#
#     return formats()


def check_format_installed(cli, to_check):
    "Checks a foramt is installed"
    subprocess.run([cli, '--format', to_check], check=True)


@pytest.mark.test_cli
def test_gdal_format_installed(gdal_format):
    "Checks a format is installed"
    check_format_installed('gdalinfo', gdal_format)


@pytest.mark.test_cli
def test_ogr_format_installed(ogr_format):
    "Checks a format is installed"
    check_format_installed('ogrinfo', ogr_format)


def check_format_excluded(cli, to_check):
    try:
        check_format_installed(cli, to_check)
        installed = True
    except subprocess.CalledProcessError:
        installed = False
    assert not installed


@pytest.mark.test_cli
def test_gdal_format_excluded(gdal_format_excluded):
    "Checks a format is excluded from the buid"
    check_format_excluded('gdalinfo', gdal_format_excluded)


@pytest.mark.test_cli
def test_ogr_format_excluded(ogr_format_excluded):
    check_format_excluded('ogrinfo', ogr_format_excluded)


@pytest.mark.test_cli
@pytest.mark.test_version_is
def test_version_is(version_to_check):
    version_to_check = version_to_check.replace('.', '\.')
    output = subprocess.run(['gdalinfo', '--version'], stdout=subprocess.PIPE)
    assert re.match(version_to_check, output.stdout.decode())

import click
import subprocess
import logging
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
# ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def check_format_installed(cli, to_check, is_present=True):
    "Checks a foramt is installed"
    if to_check == 'postgis' or to_check == 'postgresql':
        to_check = 'postgresql/postgis'
    try:
        subprocess.run(
            [cli, '--format', to_check], check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if not is_present:
            raise AssertionError(to_check + ' is unexpectedly present')
    except subprocess.CalledProcessError:  # as err
        # logger.debug(err.args)
        if is_present:
            raise AssertionError(to_check + ' is unexpectedly absent')


def style_check(cli, to_check, is_present=True):
    _cli = cli.replace('info', '')
    if cli not in ['gdalinfo', 'ogrinfo']:
        cli = 'gdalinfo' if 'gdal' in cli else 'ogrinfo'
    try:
        check_format_installed(cli, to_check, is_present)
        click.echo('{}:{}\t{}'.format(
            _cli,
            to_check,
            click.style('✓', fg='green')
            )
        )
        return True
    except AssertionError as err:
        click.echo('{}:{}\t{}\t{}'.format(
            _cli,
            to_check,
            click.style('×', fg='red'),
            click.style(err.args[0], fg='red')
            )
        )
        return False


def main(ogr_include, ogr_exclude, gdal_include, gdal_exclude):
    result = True
    for fmt in sorted(list(gdal_include)):
        result &= style_check('gdalinfo', fmt, is_present=True)
    for fmt in sorted(list(ogr_include)):
        result &= style_check('ogrinfo', fmt, is_present=True)
    for fmt in sorted(list(gdal_exclude)):
        result &= style_check('gdalinfo', fmt, is_present=False)
    for fmt in sorted(list(ogr_exclude)):
        result &= style_check('ogrinfo', fmt, is_present=False)
    return result


def test_version_is(expected):
    called = subprocess.run(
        ['gdalinfo', '--version'], check=True, stdout=subprocess.PIPE
    )
    actual = called.stdout.decode()
    if expected == re.search('\d+\.\d+\.\d+', actual).group(0):
        click.echo(click.style(expected, fg='green'))
        return True
    else:
        click.echo('expected:{}\tactual:{}'.format(
            click.style(expected, fg='green'),
            click.style(actual, fg='red')
            )
        )
        return False
    # ire.search(r'(^~\*)|(<>)?(=)?(\d+)\.(\d.)\.(\d)', version).groups()
    # npm_vr, op, eq, expected_major, expected_minor, expected_patch = expected
    # parser = re.compile(r'^GDAL (\d+)\.(\d+)\.(\d+)')
    # parsed = parser.search(called.stdout.decode())
    # major, minor, patch = map(int, parsed.groups())

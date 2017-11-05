# -*- coding: utf-8 -*-
"""Console script for gdal_build_debug."""

import os
# import subprocess
import click
import pickle
import logging
from config_test_fns import main as test_config_log
from cli_test_fns import main as test_formats, test_version_is

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


def debrine(pkl):
    "load pickled sets of normalized format codes"
    with open(__location__ + '/' + pkl, 'rb') as _pkl:
        return pickle.load(_pkl)


@click.group()
@click.option(
    '--with', 'include', multiple=True, envvar='WITH',
    help='Dependancies or formats to include in the GDAL build ' +
    'added to the whitespace-separated list in the environment variable' +
    ' WITH',
    # short_help='dependencies/formats to include in build (added to $WITH)',
    metavar='<included_lib...>'
)
@click.option(
    '--without', 'exclude', envvar='WITHOUT', multiple=True,
    help='Dependancies or formats to exclude from the GDAL build ' +
    'added to the whitespace-separated list in the environment variable' +
    ' WITHOUT',
    # short_help='dependencies/formats to exclude (added to $WITH)',
    metavar='<excluded_lib...>'
)
@click.pass_context
def main(ctx, include, exclude):
    """An assistant for common operations while building GDAL from source"""
    include = [i.lower() for i in include]
    exclude = [i.lower() for i in exclude]
    ctx.obj['INCLUDED_FORMATS_GDAL'] = gdal.intersection(include)
    ctx.obj['EXCLUDED_FORMATS_GDAL'] = gdal.intersection(exclude)
    ctx.obj['INCLUDED_FORMATS_OGR'] = ogr.intersection(include)
    ctx.obj['EXCLUDED_FORMATS_OGR'] = ogr.intersection(exclude)
    ctx.obj['INCLUDED_DEPENDENCIES'] = dependencies.intersection(include)
    ctx.obj['EXCLUDED_DEPENDENCIES'] = dependencies.intersection(exclude)
    logger.debug('included: {}'.format(include))
    logger.debug('excluded: {}'.format(exclude))
    logger.debug(
        'included ogr formats: {}'.format(ctx.obj['INCLUDED_FORMATS_OGR'])
    )
    logger.debug(
        'excluded ogr formats: {}'.format(ctx.obj['EXCLUDED_FORMATS_OGR'])
    )
    logger.debug(
        'included gdal formats {}'.format(ctx.obj['INCLUDED_FORMATS_GDAL'])
    )
    logger.debug(
        'excluded gdal formats {}'.format(ctx.obj['EXCLUDED_FORMATS_GDAL'])
    )


@main.command(short_help='test dependencies/format support/gdal version')
@click.option(
    '--path-to-config-log', 'config_log_path', default='./configure.log',
    envvar='PATH_TO_GDAL_CONFIG_LOG', type=click.Path(),
    help='a relative or absolute path to the logged output of gdal/configure'
)
@click.option(
    '--formats', is_flag=True, default=False,
    help='whether to test the command line gdal/ogr utilities for format \
    availabilities'
)
@click.option(
    '--dependencies', is_flag=True, default=False,
    help='whether to run tests on the support libraries available at the \
    command line after building'
)
@click.option(
    '--version-is', 'version_is', type=str,
    help="Tests whether the cli version is correct via regex"
)
@click.option(
    '--search', 'searches', type=str, envvar='CONFIG_LOG_SEARCHES',
    multiple=True,
    help='custom searches using regular expressions from python\'s `re` \
     module.  To use the default f'
)
@click.pass_context
def test(ctx, config_log_path, dependencies, formats, version_is, searches):
    it_works = True

    if dependencies:
        with open(config_log_path) as config_log_file:
            config_log = config_log_file.read()
            it_works &= test_config_log(
                config_log,
                ctx.obj['INCLUDED_DEPENDENCIES'],
                ctx.obj['EXCLUDED_DEPENDENCIES'],
                searches
            )
    if formats:
        it_works &= test_formats(
            ctx.obj['INCLUDED_FORMATS_GDAL'],
            ctx.obj['INCLUDED_FORMATS_OGR'],
            ctx.obj['EXCLUDED_FORMATS_GDAL'],
            ctx.obj['EXCLUDED_FORMATS_OGR']
        )

    if version_is:
        it_works &= test_version_is(version_is)

if __name__ == "__main__":
    ogr = debrine('ogr_formats_set.pkl')
    gdal = debrine('gdal_formats_set.pkl')
    dependencies = debrine('dependencies_set.pkl')
    main(obj={})

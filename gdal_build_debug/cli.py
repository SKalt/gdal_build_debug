# -*- coding: utf-8 -*-
"""Console script for gdal_build_debug."""

import os
import subprocess
import click
import pickle
import logging

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
    help='A dependancy or format to test is included in the gdal build'
)
@click.option(
    '--without', 'exclude', envvar='WITHOUT', multiple=True,
    help='A dependancy or format to test is excluded in the gdal build'
)
@click.pass_context
def main(ctx, include, exclude):
    """Console script for gdal_build_debug."""
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


@main.command()
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
@click.argument('args', nargs=-1)
@click.pass_context
def test(ctx, config_log_path, dependencies, formats, version_is, args):

    def map_to_options(arg_name, ctx_name):
        print(arg_name, ctx.obj[ctx_name], '\n\n')
        return [arg_name + '=' + arg for arg in ctx.obj[ctx_name]]

    tests = ['--path-to-config-log=' + i for i in [config_log_path] if i]
    tests += ['--version-is=' + str(version_is) if version_is else '']
    if formats:
        tests += ['--test-formats']
        tests += map_to_options(
            '--with-ogr-format',
            'INCLUDED_FORMATS_OGR'
        )
        tests += map_to_options(
            '--without-ogr-format',
            'EXCLUDED_FORMATS_OGR'
        )
        tests += map_to_options(
            '--with-gdal-format',
            'INCLUDED_FORMATS_GDAL'
        )
        tests += map_to_options(
            '--without-gdal-format',
            'EXCLUDED_FORMATS_GDAL'
        )
    if dependencies:
        tests += ['--test-dependencies']
        tests += map_to_options(
            '--with-dependency',
            'INCLUDED_DEPENDENCIES'
        )
        tests += map_to_options(
            '--without-dependency',
            'EXCLUDED_DEPENDENCIES'
        )
    logger.debug('pytest ' + __location__ + ' ' + ' '.join(tests))
    subprocess.run(
        ['pytest', __location__] + [test for test in tests if test]
    )  # TODO: filter by invocation https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests


if __name__ == "__main__":
    ogr = debrine('ogr_formats_set.pkl')
    gdal = debrine('gdal_formats_set.pkl')
    dependencies = debrine('dependencies_set.pkl')
    main(obj={})

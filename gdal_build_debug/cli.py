# -*- coding: utf-8 -*-
"""Console script for gdal_build_debug."""

import os
import re
import subprocess
import click
import pickle

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


def debrine(cli):
    "load pickled sets of normalized format codes"
    with open(cli + '_formats_set.pkl', 'rb') as pkl:
        return pickle.load(pkl)


def sort(fmt):
    "sorts --with and --without by belonging to ogr/gdal / the dependencies"
    pass


@click.group()
@click.option('--with', 'include', multiple=True, help='A dependancy or ' +
              'format to test is included in the gdal build'
              )
@click.option('--without', 'exclude', multiple=True, help='A dependancy or ' +
              'format to test is excluded in the gdal build'
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


@main.command()
@click.option(
    '--path-to-config-log', 'config_log_path', default='./configure.log',
    type=click.Path(),
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
    print(tests, '************')
    subprocess.run(
        ['pytest', __location__, *[test for test in tests if test]]
    )


if __name__ == "__main__":
    ogr = debrine('ogr')
    gdal = debrine('gdal')
    with open(os.path.join(__location__, 'supported.txt')) as f:
        dependencies = set([i.strip().lower() for i in f.read().split('\n')])
    main(obj={})

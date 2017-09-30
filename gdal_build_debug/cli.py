# -*- coding: utf-8 -*-
"""Console script for gdal_build_debug."""

import os
import re
import subprocess
import click

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


@click.group()
@click.pass_context
def main(ctx):
    """Console script for gdal_build_debug."""
    pass
    # TODO: use an option to format a config command, build command
    # TODO: delegate to helpers like 'search_config' here

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
    include_test = re.compile(r'(?i)^with[-:=](?P<lib_or_format>\w+)')
    exclude_test = re.compile(r'(?i)^without[-:=](?P<lib_or_format>\w+)')
    included = []
    excluded = []
    print(config_log_path)
    for arg in args:
        _include = re.search(include_test, arg)
        if _include and _include.group('lib_or_format'):
            included.append(_include.group('lib_or_format'))
            continue
        _exclude = re.search(exclude_test, arg)
        if _exclude and _exclude.group('lib_or_format'):
            excluded.append(_exclude.group('lib_or_format'))
            continue
        else:
            included.append(arg)
    ctx.obj['INCLUDED'] = included
    ctx.obj['EXCLUDED'] = excluded
    tests = ['--path-to-config-log=' + i for i in [config_log_path] if i]
    tests += ['--version-is=' + str(version_is) if version_is else '']
    tests += ['--test-dependencies' if dependencies else '']
    tests += ['--test-formats' if formats else '']
    tests += [
        *map(lambda arg: '--with=' + arg, included),
        *map(lambda arg: '--without=' + arg, excluded)
    ]
    print(tests)
    subprocess.run(
        ['pytest', __location__, *[test for test in tests if test]]
    )



if __name__ == "__main__":
    main(obj={})

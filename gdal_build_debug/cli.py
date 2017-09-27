# -*- coding: utf-8 -*-

"""Console script for gdal_build_debug."""

import click
#import subprocess
import os
#from gdal_build_debug import search_config
import re
# http://click.pocoo.org/5/advanced/#forwarding-unknown-options

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


@main.command()
@click.option(
    '--path-to-config-log', 'config_log_path', default='./configure.log',
    type=click.Path(),
    help='a relative or absolute path to the logged output of gdal/configure'
)
@click.option(
    '--config', is_flag=True, default=False,
    help='whether to test the configuration log for library availabilities'
)
@click.option(
    '--cli', is_flag=True, default=False,
    help='whether to run tests on the formats available at the command line \
    after building'
)
@click.argument('args', nargs=-1)
@click.pass_context
def test(ctx, config_log_path, config, cli, args):
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
    if config:
        click.echo([config_log_path, included, excluded])
    if cli:
        click.echo([config_log_path, included, excluded])
        # subprocess.run(['pytest', __location__, '--cli',
        #  *map(lambda arg: '--with=' + arg, included),
        #  *map(lambda arg: '--without=' + arg, excluded)
        #   ])

if __name__ == "__main__":
    main(obj={})

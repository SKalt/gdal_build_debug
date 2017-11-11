# -*- coding: utf-8 -*-
"""Console script for gdal_build_debug."""

import os
# import subprocess
import click
import pickle
import logging
from pprint import pprint
from config_test_fns import main as test_config_log
from cli_test_fns import main as test_formats
from cli_test_fns import test_version_is

# establish globals

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
debug = logger.debug


__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


def debrine(pkl):
    "load pickled sets of normalized format codes"
    with open(os.path.join(__location__, 'pickles', pkl), 'rb') as _pkl:
        return pickle.load(_pkl)


def lookup(name, obj):
    'lookup .-separated path from nested dict'
    for path in name.split('.'):
        obj = obj[path]
    return obj


def setify(d):
    '''
    coerces all lists in nested dict to sets. Note this modifies the nested
    dict in-place.
    '''
    if type(d) is list:
        return set(d)
    elif type(d) is dict:
        for k, v in d.items():
            d[k] = setify(v)
        return d
    else:
        return d


@click.group()
@click.option(
    '--with', 'include', multiple=True, envvar='WITH',
    help='Dependancies, formats, or options to include in the GDAL ' +
    'build added to the whitespace-separated list in the environment ' +
    'variable WITH',
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
@click.option(
    '--debug', is_flag=True,
    help='whether to include debug logging', default=False
)
# @click.option(
#     '--quiet', '-q', is_flag=True, help='whether to silence all stdout'
# )
@click.pass_context
def main(ctx, include, exclude, debug):
    """An assistant for common operations while building GDAL from source"""
    def get(name): return lookup(name, ctx.obj)

    def add(flag, to=''):
        get(to).add(flag)

    def check(flag, arg):
        if flag in options['require_arguments'] and not arg:
            raise TypeError(flag + ' requires an argument & none given')
        if flag in options['flags'] and arg:
            raise TypeError(
                '{} takes 0 arguments yet {} given'.format(flag, arg)
            )

    # if verbose:
    ctx.obj['LEVEL'] = logging.DEBUG if debug else logging.INFO
    # if quiet:
    #     pass
    ch.setLevel(ctx.obj['LEVEL'])
    include = [i.lower().partition('=') for i in include]
    exclude = [i.lower() for i in exclude]
    for flag, _, arg in include:
        complete_flag = '{}={}'.format(flag, arg)
        add(flag, to='INCLUDED.DEPENDENCIES')
        try:
            check(flag, arg)
            if flag in options['includable']:
                if flag in options['package']:
                    add(complete_flag, to='INCLUDED.PACKAGES')
            elif flag in options['config']:
                add(complete_flag, to='INCLUDED.OPTIONS')
        except TypeError:
            click.echo(click.style(flag + ' requires an argument', fg='red'))

        if flag in ogr:
            add(flag, to='INCLUDED.FORMATS.OGR')
            # add(flag, to='INCLUDED.DEPENDENCIES')

        elif flag in gdal:
            add(flag, to='INCLUDED.FORMATS.GDAL')
            # add(flag, to='INCLUDED.DEPENDENCIES')

        # if flag in dependencies:
        #     add(flag, to='INCLUDED.DEPENDENCIES')
    for flag in exclude:
        add(flag, 'EXCLUDED.DEPENDENCIES')
        if flag in gdal:
            add(flag, 'EXCLUDED.FORMATS.GDAL')
            # add(flag, 'EXCLUDED.DEPENDENCIES')
        elif flag in ogr:
            add(flag, 'EXCLUDED.FORMATS.OGR')
            # add(flag, 'EXCLUDED.DEPENDENCIES')

        if flag in options['package']:
            add(flag, 'EXCLUDED.PACKAGES')
        # if flag in dependencies:
            # add(flag, 'EXCLUDED.DEPENDENCIES')

    if ch.level == logging.DEBUG:
        pprint(ctx.obj)


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
                ctx.obj['INCLUDED']['DEPENDENCIES'],
                ctx.obj['EXCLUDED']['DEPENDENCIES'],
                searches,
                level=ctx.obj['LEVEL']
            )
    if formats:
        it_works &= test_formats(
            ogr_include=ctx.obj['INCLUDED']['FORMATS']['OGR'],
            ogr_exclude=ctx.obj['EXCLUDED']['FORMATS']['OGR'],
            gdal_exclude=ctx.obj['EXCLUDED']['FORMATS']['GDAL'],
            gdal_include=ctx.obj['INCLUDED']['FORMATS']['GDAL'],
            level=ctx.obj['LEVEL']
        )

    if version_is:
        it_works &= test_version_is(version_is)


@main.command(
    'config-command', short_help="echo a gdal configuration[, make] command"
)
@click.option(
    '--path-to-config-command', '-c', type=str, default='./configure',
    help='the path to the gdal configuration script'
    # store as internal variable?
)
@click.option('--save-to', default='', help='if/where to save the command')
# @click.option('--cols', type=int, default=1)
# @click.option('--max-width', type=int, default=80)
# @click.option('--make', is_flag=True, help='include the make command') # TODO
@click.pass_context
def command(ctx, path_to_config_command, save_to):
    def get(name): return lookup(name, ctx.obj)
    included = get('INCLUDED.PACKAGES')
    excluded = get('EXCLUDED.PACKAGES')
    command = [path_to_config_command] + \
        ['    --with-' + fmt for fmt in included] + \
        ['    --without-' + fmt for fmt in excluded]
    command = ' \\\n'.join(command)
    # if make:
    #   command = 'make clean\n' + command + 'make\nmake install'
    click.echo(command)
    if save_to:
        with open(save_to, 'w') as target:
            target.write(command)


if __name__ == "__main__":
    # TODO: set all this up in setup-scripts and debrine this as a tuple
    ogr = debrine('ogr_formats_set.pkl')
    gdal = debrine('gdal_formats_set.pkl')
    formats = gdal.union(ogr)
    dependencies = debrine('dependencies_set.pkl')
    options = {  # setify(json.loads(os.path.join(__location__, '...')))
        'excludable': debrine('excluded_flags.pkl'),
        'includable': debrine('included_flags.pkl'),
        'flags': debrine('flags.pkl'),
        'require_arguments': debrine('options_requiring_argument.pkl'),
        'has_default': debrine('options_with_default.pkl')
    }
    options['all'] = options['includable']\
        .union(options['excludable'])\
        .union(options['require_arguments'])\
        .union(options['has_default'])\
        .union(options['flags'])
    options['package'] = options['includable'].union(options['excludable'])
    options['config'] = options['all'].difference(options['package'])
    main(obj={
        'INCLUDED': {
            'FORMATS': {           # for format test
                'GDAL': set(),
                'OGR': set()
            },
            'OPTIONS': set(),       # for command building
            'DEPENDENCIES': set(),  # for config testing
            'PACKAGES': set()       # for command building
        },
        'EXCLUDED': {
            'FORMATS': {            # for format test
                'GDAL': set(),
                'OGR': set()
            },
            'DEPENDENCIES': set(),  # for config test
            'PACKAGES': set()       # for command building
        }
    })

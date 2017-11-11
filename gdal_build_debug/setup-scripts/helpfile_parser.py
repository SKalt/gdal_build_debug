import re
# import logging
import json
import os

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# ch = logging.StreamHandler()
# ch.setFormatter(formatter)
# ch.setLevel(logging.DEBUG)
# logger.addHandler(ch)
# debug = logger.debug


search = re.compile(
    r'(?is)' +
    r'\s+--?' +
    r'(?P<inclusion>' +
        r'(?P<with>with)?(?P<out>out)?-?' +
    r')?' +
    r'(' +
        r'(?P<opt>[\w\-]+)' +
        r'(?P<argContext>\[?=(?P<arg>\S+)\]?)?' +
    r')' +
    r'\s+(?P<help>[^\(\[\n]+)' +
    r'(' +
        r'(' +
            r'\((?P<argVal>[^\-\)]*)\)' +
        r')?[^\n\[]*' +
        r'(\[' +
            r'(?P<default>(default=)?([^\]]*)' +
        r'\])' +
    r')?)'
)


def process(match, included, excluded, flags, optionals, required):
    '''
    sort gdal/configure options into flags (no arguments taken), optionals
    (take an omittable argument), and required (must take an argument). All
    package inclusion flags (--with/without) are also sorted.
    '''
    def get_group(name):
        try:
            return match.group(name)
        except IndexError:
            print(name)
            raise IndexError(name)
    groups = ['with', 'out', 'opt', 'argContext', 'arg', 'argVal', 'default']
    include, exclude, opt, _arg, arg, arg_val, opt_default = map(
        get_group, groups
    )
    if 'PACKAGE' not in opt and 'FEATURE' not in opt:
        if exclude:  # a --without-PACKAGE flag
            excluded.add(opt)
        elif include:  # a --with-PACKAGE flag
            included.add(opt)
        if _arg:  # can take an argument
            if '[' in _arg or opt_default:
                optionals.add(opt)
            else:
                required.add(opt)
        else:
            flags.add(opt)

    return included, excluded, flags, optionals, required


def extract_flags(usage):
    included, excluded, flags, optionals, required = [set() for i in range(5)]
    for match in search.finditer(usage):
        process(match, included, excluded, flags, optionals, required)
    return included, excluded, flags, optionals, required


def preserve(set_obj, name):
    loc = os.path.join(__location__, '..', 'json', name + '.json')
    with open(loc, 'w') as target:
        target.write(json.dumps(list(set_obj)))


if __name__ == '__main__':
    loc = os.path.join(
        __location__, '..', 'reference-documents', 'helpfile.txt'
        )
    with open(loc) as helpfile:
        usage = helpfile.read()
    included, excluded, flags, optionals, required = extract_flags(usage)
    preserve(included, 'included_flags')
    preserve(excluded, 'excluded_flags')
    preserve(flags, 'flags')
    preserve(optionals, 'options_with_default')
    preserve(required, 'options_requiring_argument')

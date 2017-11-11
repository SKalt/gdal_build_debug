import pandas as pd
from lxml import html
import json  # for faster loading of cli
import os
import logging


__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
ch = logging.StreamHandler()
# ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
debug = logger.debug


def abs_path_to(relative_path, *args):
    return os.path.join(__location__, *relative_path.split('/')).format(*args)


def parse(url):
    """
    scrape the formats table at the url and save it as a csv and pickled set of
    normalized codes
    """
    page = html.parse(url)
    header = [' '.join(i.xpath('.//text()')) for i in page.xpath('//tr/th')]
    debug('csv header: {}'.format(header))
    rows = page.xpath('//tr[not(position()=1)]')
    processed_rows = []
    for row in rows:
        _row = []
        # print('\n\n\n')
        for cell in row.xpath('.//td'):
            # print(cell.xpath('.//text()'))
            _row.append(' '.join(cell.xpath('.//text()')).strip())
        processed_rows.append(_row)
    cli = 'ogr' if 'ogr' in url else 'gdal'
    df = pd.DataFrame(processed_rows)
    df.columns = header
    target_csv = abs_path_to('../reference-documents/{}_formats.csv', cli)
    df.to_csv(target_csv, index=False, header=header)
    to_store = set(df['Code'].apply(lambda code: code.lower().strip()))
    for split in [item.split('/') for item in to_store if '/' in item]:
        for part in split:
            to_store.add(part)
    json_target = abs_path_to('../json/{}_formats_set.json', cli)
    with open(json_target, 'w') as target:
        json.dump(list(to_store), target)


def update_supported():
    'update the pickled set of gdal dependencies'
    with open(
        os.path.join(
            __location__, '..', 'reference-documents', 'supported.txt'
            )
    ) as libs:
        # supported.txt is from concatenating ogr and gdal formats, with some
        # judicious word-splitting
        to_store = {i.lower().strip() for i in libs.read().split('\n')}
        target_location = abs_path_to('../json/dependencies_set.json')
        with open(target_location, 'w') as target:
            json.dump(list(to_store), target)


if __name__ == '__main__':
    ogr_url = 'http://www.gdal.org/ogr_formats.html'
    gdal_url = 'http://www.gdal.org/formats_list.html'
    parse(ogr_url)
    parse(gdal_url)
    update_supported()

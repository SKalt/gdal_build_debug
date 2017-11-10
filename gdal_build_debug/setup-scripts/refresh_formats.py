import pandas as pd
from lxml import html
import pickle  # for faster loading of cli
import os

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


def parse(url):
    """
    scrape the formats table at the url and save it as a csv and pickled set of
    normalized codes
    """
    page = html.parse(url)
    header = [' '.join(i.xpath('.//text()')) for i in page.xpath('//tr/th')]
    print(header)
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
    df.to_csv(cli + '_formats.csv', index=False, header=header)
    to_pickle = set(df['Code'].apply(lambda code: code.lower().strip()))
    for split in [item.split('/') for item in to_pickle if '/' in item]:
        for part in split:
            to_pickle.add(part)
    pickle.dump(to_pickle, open(cli + '_formats_set.pkl', 'wb'))


def update_supported():
    'update the pickled set of gdal dependencies'
    with open(
        os.path.join(
            __location__, '..', 'reference-documents', 'supported.txt')
    ) as libs:
        # supported.txt is from concatenating ogr and gdal formats, with some
        # judicious word-splitting
        to_pickle = {i.lower().strip() for i in libs.read().split('\n')}
        with open('dependencies_set.pkl', 'wb') as target:
            pickle.dump(to_pickle, target)


if __name__ == '__main__':
    ogr_url = 'http://www.gdal.org/ogr_formats.html'
    gdal_url = 'http://www.gdal.org/formats_list.html'
    parse(ogr_url)
    parse(gdal_url)
    update_supported()
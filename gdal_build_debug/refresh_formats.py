import pandas as pd
from lxml import html


def parse(url):
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
    ogr = 'ogr' if 'ogr' in url else 'gdal'
    pd.DataFrame(processed_rows).to_csv(
        ogr + '_formats.csv', index=False, header=header
    )


if __name__ == '__main__':
    ogr_url = 'http://www.gdal.org/ogr_formats.html'
    gdal_url = 'http://www.gdal.org/formats_list.html'
    parse(ogr_url)
    parse(gdal_url)

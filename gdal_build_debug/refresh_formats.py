import pandas as pd
from lxml import html
import pickle  # for faster loading


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
    pickle.dump(
        set(df['Code'].apply(lambda code: code.lower().strip())),
        open(cli + '_formats_set.pkl', 'wb')
    )


if __name__ == '__main__':
    ogr_url = 'http://www.gdal.org/ogr_formats.html'
    gdal_url = 'http://www.gdal.org/formats_list.html'
    parse(ogr_url)
    parse(gdal_url)

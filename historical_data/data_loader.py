import requests
from lxml import html
from datetime import datetime
from historical_data.models import HistoricalRecord

HISTORICAL_DATA_TEMPLATE_URL = 'http://www.nasdaq.com/symbol/{ticker}/historical'
commas_filter = str.maketrans('', '', ',')


def load_historical_data(ticker_list):
    for ticker in ticker_list:
        url = HISTORICAL_DATA_TEMPLATE_URL.format(ticker=ticker)

        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.content

            doc = html.fromstring(html_content)

            table_rows = doc.xpath('//div[@id="historicalContainer"]/div/table/tbody/tr')

            historical_records = []
            for row in table_rows[1:]:
                cells = row.xpath('td/text()')

                historical_records.append(HistoricalRecord(
                    ticker=ticker.upper(),
                    date=datetime.strptime(cells[0].strip(), '%m/%d/%Y').date(),
                    open_price=float(cells[1].strip()),
                    high_price=float(cells[2].strip()),
                    low_price=float(cells[3].strip()),
                    close_price=float(cells[4].strip()),
                    volume=float(cells[5].strip().translate(commas_filter))
                ))

            HistoricalRecord.objects.bulk_create(historical_records)


def load_insider_data():
    pass

from django.db.models import QuerySet, Q


class HistoricalRecordQuerySet(QuerySet):

    def price_diff(self, ticker, from_date, to_date):
        records = self.filter(Q(date=from_date) | Q(date=to_date), ticker=ticker).order_by('date')

        if len(records) == 2:
            return {
                'open_price_diff': records[1].open_price - records[0].open_price,
                'high_price_diff': records[1].high_price - records[0].high_price,
                'low_price_diff': records[1].low_price - records[0].low_price,
                'close_price_diff': records[1].close_price - records[0].close_price,
            }
        else:
            return None

    def price_delta(self, ticker, value, price_type):
        if price_type not in ('open', 'high', 'low', 'close'):
            return None

        sub_query = f'''SELECT
                    hd1 as hd1, hd2 as hd2,
                    ABS(hd1.date - hd2.date) AS date_diff,
                    ABS(hd1.{price_type}_price - hd2.{price_type}_price) AS price_diff
                FROM historical_data_historicalrecord AS hd1
                INNER JOIN historical_data_historicalrecord AS hd2
                ON hd1.ticker = hd2.ticker
                    AND ABS(hd1.{price_type}_price - hd2.{price_type}_price) > %s
                    AND hd1.date < hd2.date
                WHERE hd1.ticker = %s
                ORDER BY date_diff ASC, hd1.date ASC'''

        result = self.raw(
            f'''SELECT *
                FROM ({sub_query}) AS differences''',
            [value, ticker]
        )

        r = list(result)
        to_records = self.in_bulk([row.second_id for row in result])

        return ({
            'from_record': row,
            'to_record': to_records.get(row.second_id),
            'date_diff': row.date_diff,
            'price_diff': row.price_diff
        } for row in result)

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

        result = self.raw(
            f'''SELECT MIN(ABS(hd1.date - hd2.date)) FROM historical_data_historicalrecord AS hd1
                INNER JOIN historical_data_historicalrecord AS hd2
                ON ABS(hd1.{price_type}_price - hd2.{price_type}_price) > %s
                WHERE hd1.ticker = %s AND hd2.ticker = %s''',
            [value, ticker, ticker]
        )

        return list(result)

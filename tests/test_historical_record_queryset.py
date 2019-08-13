import pytest
from datetime import date

from historical_data.models import HistoricalRecord


@pytest.fixture
def records(historical_record_factory):
    return [
        historical_record_factory('AAPL', date(2019, 1, 1), 100.0, 132.0, 100.0, 134.0, 1000000),
        historical_record_factory('AAPL', date(2019, 1, 2), 102.0, 345.0, 100.0, 134.0, 1000000),
        historical_record_factory('AAPL', date(2019, 1, 3), 104.0, 345.0, 100.0, 134.0, 1000000),
        historical_record_factory('AAPL', date(2019, 1, 4), 106.0, 345.0, 100.0, 134.0, 1000000),
        historical_record_factory('AAPL', date(2019, 1, 5), 108.0, 23.0, 10.0, 12.5, 1000000),
        historical_record_factory('AAPL', date(2019, 1, 6), 107.0, 23.0, 10.0, 12.5, 1000000),
        historical_record_factory('AAPL', date(2019, 1, 7), 106.0, 23.0, 10.0, 12.5, 1000000),
        historical_record_factory('AAPL', date(2019, 1, 8), 109.0, 23.0, 10.0, 12.5, 1000000),
        historical_record_factory('AAPL', date(2019, 1, 9), 104.0, 23.0, 10.0, 12.5, 1000000),
    ]


@pytest.mark.django_db
def test_price_diff(records):

    price_diff = HistoricalRecord.objects.price_diff('AAPL', date(2019, 1, 1), date(2019, 1, 5))

    assert(price_diff['open_price_diff'] == 8.0)
    assert(price_diff['high_price_diff'] == -109.0)
    assert(price_diff['low_price_diff'] == -90.0)
    assert(price_diff['close_price_diff'] == -121.5)

    price_diff = HistoricalRecord.objects.price_diff('AAPL', date(2019, 1, 1), date(2019, 1, 20))

    assert(price_diff is None)


@pytest.mark.django_db
def test_price_delta(records):
    price_delta = HistoricalRecord.objects.price_delta('AAPL', 8, 'open')

    assert(price_delta['first'].date == date(2019, 1, 5))
    assert(price_delta['second'].date == date(2019, 1, 6))

    price_delta = HistoricalRecord.objects.price_delta('AAPL', 106, 'open')

    assert(price_delta['first'].date == date(2019, 1, 3))
    assert(price_delta['second'].date == date(2019, 1, 5))

    price_delta = HistoricalRecord.objects.price_delta('AAPL', 1006, 'open')

    assert(price_delta is None)

    price_delta = HistoricalRecord.objects.price_delta('AAPL', 1, 'open')

    assert(price_delta['first'].date == date(2019, 1, 1))
    assert(price_delta['second'].date == date(2019, 1, 2))

import pytest
from datetime import date

from historical_data.models import HistoricalRecord


@pytest.fixture
def records(historical_record_factory):
    return [
        historical_record_factory('AAPL', date(2019, 1, 1), 123.0, 132.0, 100.0, 134.0, 1000000),
        historical_record_factory('AAPL', date(2019, 1, 2), 125.0, 345.0, 100.0, 134.0, 1000000),
        historical_record_factory('AAPL', date(2019, 1, 3), 128.0, 345.0, 100.0, 134.0, 1000000),
        historical_record_factory('AAPL', date(2019, 1, 4), 124.0, 345.0, 100.0, 134.0, 1000000),
        historical_record_factory('AAPL', date(2019, 1, 5), 23.0, 23.0, 10.0, 12.5, 1000000),
    ]


@pytest.mark.django_db
def test_price_diff(records):

    price_diff = HistoricalRecord.objects.price_diff('AAPL', date(2019, 1, 1), date(2019, 1, 5))

    assert(price_diff['open_price_diff'] == -100.0)
    assert(price_diff['high_price_diff'] == -109.0)
    assert(price_diff['low_price_diff'] == -90.0)
    assert(price_diff['close_price_diff'] == -121.5)

    price_diff = HistoricalRecord.objects.price_diff('AAPL', date(2019, 1, 1), date(2019, 1, 20))

    assert(price_diff is None)


@pytest.mark.django_db
def test_price_delta(records):
    price_delta = HistoricalRecord.objects.price_delta('AAPL', 5, 'open')

    pass

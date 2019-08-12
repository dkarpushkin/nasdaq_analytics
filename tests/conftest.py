import pytest

from historical_data.models import HistoricalRecord


@pytest.fixture
def historical_record_factory():
    def _make_historical_record(ticker, date, open_price, high, low, close, volume):
        return HistoricalRecord.objects.create(
            ticker=ticker,
            date=date,
            open_price=open_price,
            high_price=high,
            low_price=low,
            close_price=close,
            volume=volume
        )

    return _make_historical_record

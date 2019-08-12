from django.db import models

from historical_data.querysets import HistoricalRecordQuerySet


class HistoricalRecord(models.Model):
    """
    Запись цен
    """
    ticker = models.CharField(max_length=16, db_index=True)
    date = models.DateField(db_index=True)

    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.FloatField()

    objects = HistoricalRecordQuerySet.as_manager()

    class Meta:
        verbose_name = 'Historical Record'

    def as_dict(self):
        return {
            'ticker': self.ticker,
            'date': self.date,
            'open_price': self.open_price,
            'high_price': self.high_price,
            'low_price': self.low_price,
            'close_price': self.close_price,
            'volume': self.volume,
        }

from django.core.management import BaseCommand

from historical_data.data_loader import load_historical_data, load_insider_data


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('tickers_list_file', type=str)

    def handle(self, *args, **options):
        tickers_list_file = options.get('tickers_list_file')

        with open(tickers_list_file, 'r') as f:
            ticker_list = [ticker.strip() for ticker in f.read().split(',')]

            load_historical_data(ticker_list)
            load_insider_data()

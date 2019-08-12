from datetime import datetime

from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, TemplateView

from historical_data.models import HistoricalRecord


class HistoricalRecordsView(ListView):
    model = HistoricalRecord
    queryset = model.objects.all()
    ordering = ('-date',)

    def get_queryset(self):
        return super().get_queryset().filter(ticker=self.kwargs['ticker'].upper())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        context.update({
            'ticker': self.kwargs['ticker']
        })

        return context


class HistoricalRecordsTemplateView(HistoricalRecordsView):
    template_name = 'HistoricalRecords.html'


class HistoricalRecordsJsonView(HistoricalRecordsView):

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()

        return JsonResponse([record.as_dict() for record in qs], safe=False)


class PriceAnalyticsView:

    def get_analytics(self):

        date_from = datetime.strptime(self.request.GET['date_from'], '%m/%d/%Y')
        date_to = datetime.strptime(self.request.GET['date_to'], '%m/%d/%Y')
        return HistoricalRecord.objects.price_diff(self.kwargs['ticker'].upper(), date_from.date(), date_to.date())


class PriceAnalyticsTemplateView(PriceAnalyticsView, TemplateView):
    template_name = 'PriceAnalytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'ticker': self.kwargs['ticker']
        })
        try:
            analytics = self.get_analytics()
        except:

            analytics = None

        if analytics is not None:
            context.update(self.get_analytics())

        return context


class PriceAnalyticsJsonView(PriceAnalyticsView, View):

    def get(self, request, *args, **kwargs):
        context = self.get_analytics()

        return JsonResponse(context)

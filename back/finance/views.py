from rest_framework import viewsets
from .models import DailyPrice, CommodityPrice
from .serializers import DailyPriceSerializer,CommodityPriceSerializer
from datetime import datetime, timedelta

class DailyPriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailyPrice.objects.all()
    serializer_class = DailyPriceSerializer
    lookup_field = 'code'
    def get_queryset(self):
        code = self.request.query_params.get('code')
        return self.queryset.filter(code=code).order_by('-date')[:30]

class CommodityPriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommodityPrice.objects.all().order_by('date')
    serializer_class = CommodityPriceSerializer

    def get_queryset(self):
        comm = self.kwargs.get('commodity')  # urls.py에 <str:commodity>로 설정
        years = self.request.query_params.get('years', 1)
        cutoff = datetime.today().date() - timedelta(days=365*int(years))
        return CommodityPrice.objects.filter(
            commodity=comm, date__gte=cutoff
        ).order_by('date')
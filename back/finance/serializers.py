from rest_framework import serializers
from .models import DailyPrice, CommodityPrice

class DailyPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyPrice
        fields = '__all__'


class CommodityPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommodityPrice
        # 'commodity' 필드는 to_representation()에서 꺼낼 거니까 제외해도 되고, 필요하면 넣어둬도 됩니다.
        fields = ('date', 'price', 'commodity')
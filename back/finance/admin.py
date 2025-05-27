from django.contrib import admin
from .models import CommodityPrice

@admin.register(CommodityPrice)
class CommodityPriceAdmin(admin.ModelAdmin):
    list_display  = ('commodity','date','price')
    list_filter   = ('commodity',)
    search_fields = ('commodity',)
    ordering      = ('-date',)
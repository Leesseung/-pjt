from django.db import models

class DailyPrice(models.Model):
    code     = models.CharField(max_length=10)
    date     = models.DateField()
    close    = models.IntegerField()
    open     = models.IntegerField()
    high     = models.IntegerField()
    low      = models.IntegerField()
    volume   = models.BigIntegerField()
    class Meta:
        unique_together = ('code','date')


class Company(models.Model):
    code          = models.CharField(max_length=10, unique=True)
    name          = models.CharField(max_length=100)
    current_price = models.IntegerField()
    last_close    = models.IntegerField()


class CommodityPrice(models.Model):
    commodity = models.CharField(max_length=10)
    date      = models.DateField()
    price     = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        unique_together = ('commodity','date')
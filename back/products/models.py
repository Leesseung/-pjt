# products/models.py
from django.db import models

class Product(models.Model):
    product_id    = models.CharField(max_length=64)
    save_trm      = models.IntegerField(default=0)
    intr_rate     = models.FloatField(default=0)
    supr_rate     = models.FloatField(default=0)

    # 공시 관련 날짜 필드들: null/blank 허용
    dcls_month    = models.CharField(max_length=6, blank=True, null=True)
    dcls_strt_day = models.CharField(max_length=8, blank=True, null=True)
    dcls_end_day  = models.CharField(max_length=8, blank=True, null=True)

    fin_co_no     = models.CharField(max_length=10, blank=True, null=True)
    bank_name     = models.CharField(max_length=100)
    name          = models.CharField(max_length=200)

    join_deny     = models.CharField(max_length=1, blank=True, null=True)
    join_way      = models.CharField(max_length=200, blank=True, null=True)
    spcl_cnd      = models.TextField(blank=True, null=True)
    etc_note      = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('product_id', 'save_trm')

    def __str__(self):
        return f"{self.bank_name} – {self.name}"

class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 금융상품 코드
    kor_co_nm = models.TextField() # 금융회사 명
    fin_prdt_nm = models.TextField() # 금융상품 명
    etc_note = models.TextField() # 기타 유의사항
    join_deny = models.IntegerField() # 가입제한
    join_member = models.TextField() # 가입대상
    join_way = models.TextField() # 가입방법
    spcl_cnd = models.TextField() # 우대조건

    def __str__(self):
        return self.fin_prdt_nm


class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='options') #금융 상품 명
    fin_prdt_cd = models.TextField() # 금융상품 코드
    intr_rate_type_nm = models.CharField(max_length=100) #저축 금리 유형명
    intr_rate = models.FloatField() # 저축금리
    intr_rate2 = models.FloatField() # 최고 우대 금리
    save_trm = models.IntegerField() # 저축 기간

    def __str__(self):
        return f"{self.fin_prdt_cd} - {self.save_trm}개월"

class SavingProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 금융상품 코드
    kor_co_nm = models.TextField() # 금융회사 명
    fin_prdt_nm = models.TextField() # 금융상품 명
    etc_note = models.TextField() # 기타 유의사항
    join_deny = models.IntegerField() # 가입제한
    join_member = models.TextField() # 가입대상
    join_way = models.TextField() # 가입방법
    spcl_cnd = models.TextField() # 우대조건

    def __str__(self):
        return self.fin_prdt_nm


class SavingOptions(models.Model):
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE, related_name='options') #금융 상품 명
    fin_prdt_cd = models.TextField() # 금융상품 코드
    intr_rate_type_nm = models.CharField(max_length=100) #저축 금리 유형명
    intr_rate = models.FloatField() # 저축금리
    intr_rate2 = models.FloatField() # 최고 우대 금리
    save_trm = models.IntegerField() # 저축 기간

    def __str__(self):
        return f"{self.fin_prdt_cd} - {self.save_trm}개월"
    



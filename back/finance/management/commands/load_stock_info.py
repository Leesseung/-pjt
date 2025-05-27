import json
import requests
from django.core.management.base import BaseCommand
from finance.models import Company

class Command(BaseCommand):
    help = "네이버 모바일 API로 종목명, 현재가, 시총, PER, PBR, 종가를 가져와서 DB에 저장"

    def add_arguments(self, parser):
        parser.add_argument('--code', required=True, help='종목 코드 (예: 005930)')

    def handle(self, *args, **opts):
        code = opts['code']
        headers = {'User-Agent': 'Mozilla/5.0'}

        # 1) 네이버 모바일 통합 API에서 정보 가져오기
        meta_url = f"https://m.stock.naver.com/api/stock/{code}/integration"
        resp = requests.get(meta_url, headers=headers)
        resp.raise_for_status()
        meta = resp.json()

        # 종목명, 현재가
        name = meta.get('stockName')
        current_price_raw = meta.get('dealTrendInfos', [{}])[0].get('closePrice')
        # 쉼표 제거 후 int 변환
        current_price = int(str(current_price_raw).replace(',', '')) if current_price_raw else None

        # 시총, PER, PBR 추출
        market_value = per = pbr = None
        for info in meta.get('totalInfos', []):
            if info.get('code') == 'marketValue':
                market_value_raw = info.get('value')
                # 한글 단위가 포함되어 있으므로 문자열 그대로 저장
                market_value = str(market_value_raw) if market_value_raw else None
            elif info.get('code') == 'per':
                per_raw = info.get('value')
                try:
                    per = float(str(per_raw).replace(',', '')) if per_raw else None
                except ValueError:
                    per = None
            elif info.get('code') == 'pbr':
                pbr_raw = info.get('value')
                try:
                    pbr = float(str(pbr_raw).replace(',', '')) if pbr_raw else None
                except ValueError:
                    pbr = None

        # 2) 종가(전일 종가) 가져오기
        last_close = None
        if meta.get('dealTrendInfos'):
            last_close_raw = meta['dealTrendInfos'][0].get('closePrice')
            last_close = int(str(last_close_raw).replace(',', '')) if last_close_raw else None
        # 3) DB 저장
        obj, created = Company.objects.update_or_create(
            code=code,
            defaults={
                'name':          name,
                'current_price': current_price,
                'last_close':    last_close,
                # 필요하다면 아래 항목도 모델에 추가해서 저장
                # 'market_value':   market_value,
                 'per':            per,
                 'pbr':            pbr,
            }
        )
        verb = "생성" if created else "업데이트"
        self.stdout.write(self.style.SUCCESS(
            f"{code} {verb}: [{name}] 현재가={current_price}, 종가={last_close}, 시총={market_value}, PER={per}, PBR={pbr}"
        ))
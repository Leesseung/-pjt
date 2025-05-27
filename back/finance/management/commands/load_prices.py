import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.core.management.base import BaseCommand
from finance.models import DailyPrice

class Command(BaseCommand):
    help = "네이버 일별 시세 크롤링 후 DB 저장"

    def add_arguments(self, parser):
        parser.add_argument(
            '--code', required=True,
            help='종목 코드 (예: 005930)'
        )
        parser.add_argument(
            '--pages', type=int, default=3,
            help='크롤링할 페이지 수 (기본: 3)'
        )

    def handle(self, *args, **options):
        code  = options['code']
        pages = options['pages']
        url   = os.getenv(
            'NAVER_FINANCE_URL',
            'https://finance.naver.com/item/sise_day.nhn'
        )
        headers = {'User-Agent': 'Mozilla/5.0'}
        saved_count = 0

        for page in range(1, pages + 1):
            resp = requests.get(
                url,
                params={'code': code, 'page': page},
                headers=headers
            )
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'lxml')
            rows = soup.select('table.type2 tr')[2:]

            for tr in rows:
                cols = [td.text.strip().replace(',', '') for td in tr.find_all('td')]
                if len(cols) >= 7 and cols[0]:
                    date_str, close, diff, open_p, high, low, vol = cols[:7]
                    try:
                        date = datetime.strptime(date_str, '%Y.%m.%d').date()
                    except ValueError:
                        continue

                    defaults = {
                        'close':  int(close),
                        'open':   int(open_p),
                        'high':   int(high),
                        'low':    int(low),
                        'volume': int(vol),
                    }
                    DailyPrice.objects.update_or_create(
                        code=code,
                        date=date,
                        defaults=defaults
                    )
                    saved_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"{code}: 총 {saved_count}건 저장 완료")
        )
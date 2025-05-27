import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from django.core.management.base import BaseCommand
from finance.models import CommodityPrice

class Command(BaseCommand):
    help = "금/은 최근 N년치 일별 시세 크롤링 → DB 업데이트 (소수점 둘째자리까지)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--commodity',
            choices=['gold','silver'],
            default='gold',
            help="gold 또는 silver (기본: gold)"
        )
        parser.add_argument(
            '--years',
            type=int,
            default=1,
            help="몇 년치 데이터 유지할지 (기본: 1)"
        )

    def handle(self, *args, **opts):
        comm  = opts['commodity']
        years = opts['years']
        symbol_map = {'gold': 'CMDT_GC', 'silver': 'CMDT_SI'}
        symbol = symbol_map[comm]

        url = "https://finance.naver.com/marketindex/worldDailyQuote.naver"
        headers = {'User-Agent': 'Mozilla/5.0'}
        params  = {'marketindexCd': symbol, 'fdtc': 2}

        cutoff = datetime.today().date() - timedelta(days=365 * years)
        total_saved = 0

        # 1) 페이지 순회하여 cutoff 이후 데이터만 크롤링
        for page in range(1, 999):
            params['page'] = page
            resp = requests.get(url, params=params, headers=headers)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, 'lxml')
            table = soup.select_one('table.tbl_exchange.today')
            if not table:
                self.stderr.write(f"[ERROR] 테이블을 찾을 수 없습니다 (page={page})")
                break

            # tbody tr 모두
            rows = table.select('tbody tr')
            if not rows:
                break

            stop = False
            for tr in rows:
                date_text = tr.select_one('td.date').text.strip()
                price_text = tr.select('td.num')[0].text.strip().replace(',', '')

                try:
                    date = datetime.strptime(date_text, '%Y.%m.%d').date()
                except ValueError:
                    continue

                if date < cutoff:
                    stop = True
                    break

                # 소수점 둘째 자리까지 반올림
                price = Decimal(price_text)

                # DB 저장 또는 업데이트
                CommodityPrice.objects.update_or_create(
                    commodity=comm,
                    date=date,
                    defaults={'price': price}
                )
                total_saved += 1

            if stop:
                break
            self.stdout.write(f"Page {page} 완료 (누적 {total_saved}건)")

        # 2) cutoff 이전 데이터 삭제
        deleted, _ = CommodityPrice.objects.filter(
            commodity=comm,
            date__lt=cutoff
        ).delete()

        self.stdout.write(self.style.SUCCESS(
            f"{comm}: 총 {total_saved}건 저장/업데이트, "
            f"{deleted}건 삭제 (기간: 최근 {years}년)"
        ))

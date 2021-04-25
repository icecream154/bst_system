import os, django

from django.test import TestCase

from bts.models.bank_teller import BankTeller
from bts.models.products import Fund, FundPriceRecord, Stock, StockPriceRecord

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from bts.bts_test.rpc_test import sys_register, sys_login, issue_fund, issue_stock

from django.test import Client


class TestModels(TestCase):
    def setUp(self):
        self.client = Client()
        sys_register("实体类测试", "imbus123", "柜员", "13966667777")

        status_code, response_dict = sys_login("实体类测试", "imbus123")
        bank_teller_token = response_dict['token']

        status_code, response_dict = issue_fund(bank_teller_token, "基金一号", '2021-3-20', 3.2)
        self.fund_id = response_dict['fund_id']

        status_code, response_dict = issue_stock(bank_teller_token, "招商银行", '2021-3-30', 15)
        self.stock_id = response_dict['stock_id']

    def test_models(self):
        self.assertTrue(str(BankTeller.objects.get(account="实体类测试")))

        fund = Fund.objects.get(fund_id=self.fund_id)
        fund_price_records = fund.fundpricerecord_set.all()
        for fund_price_record in fund_price_records:
            self.assertTrue(fund_price_record.to_dict())

        stock = Stock.objects.get(stock_id=self.stock_id)
        stock_price_records = stock.stockpricerecord_set.all()
        for stock_price_record in stock_price_records:
            self.assertTrue(stock_price_record.to_dict())

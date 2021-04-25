import os, django

from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from bts.bts_test.rpc_test import sys_register, sys_login, add_customer, issue_stock, buy_stock, \
    query_stock_investment_by_customer_id

from bts.models.constants import EM_INVALID_OR_MISSING_PARAMETERS

from django.test import Client


class TestStockInvestmentRecord(TestCase):
    def setUp(self):
        self.client = Client()
        sys_register("股票投资记录测试", "imbus123", "柜员", "13966667777")

        status_code, response_dict = sys_login("股票投资记录测试", "imbus123")
        self.bank_teller_token = response_dict['token']

        status_code, response_dict = add_customer(self.bank_teller_token, "客户一", "13200006789", "330888855690001",
                                                  10000000.0)
        self.customer_id = response_dict["customer_id"]

        status_code, response_dict = issue_stock(self.bank_teller_token, "浦发银行", '2021-3-20', 15)
        stock_id = response_dict['stock_id']
        buy_stock(self.bank_teller_token, self.customer_id, stock_id, 200, "2021-3-21")

    def test_query_deposits_by_customer_id(self):
        # 正确查询用户存款记录测试
        status_code, response_dict = query_stock_investment_by_customer_id(self.bank_teller_token, self.customer_id)
        self.assertEqual(200, status_code)
        self.assertEqual(1, len(response_dict))

        # 无柜员权限测试
        status_code, response_dict = query_stock_investment_by_customer_id('wrong token', self.customer_id)
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数缺失测试
        status_code, response_dict = query_stock_investment_by_customer_id(self.bank_teller_token)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

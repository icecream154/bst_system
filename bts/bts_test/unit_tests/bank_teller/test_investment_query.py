import os, django

from django.test import TestCase

from bts.models.loan import LoanRecord

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from bts.bts_test.rpc_test import sys_register, sys_login, add_customer, loan_auto_repay, issue_fund, issue_stock, \
    issue_regular_deposit, buy_fund, buy_stock, buy_regular_deposit, query_customer_fund_invest

from bts.models.constants import EM_INVALID_OR_MISSING_PARAMETERS, EM_DEPOSIT_NOT_ENOUGH, EM_CANNOT_PAY_FINE

from django.test import Client


class TestInvestmentQuery(TestCase):
    def setUp(self):
        self.client = Client()
        sys_register("投资测试", "imbus123", "柜员", "13966667777")

        status_code, response_dict = sys_login("投资测试", "imbus123")
        self.bank_teller_token = response_dict['token']

        status_code, response_dict = add_customer(self.bank_teller_token, "客户一", "13100006789", "330888855590001",
                                                  10000000.0)
        self.customer_id = response_dict["customer_id"]

        status_code, response_dict = issue_fund(self.bank_teller_token, "基金一号", '2021-3-20', 3.0)
        fund_id = response_dict['fund_id']

        buy_fund(self.bank_teller_token, self.customer_id, fund_id, 700, "2021-3-21", 100)

        status_code, response_dict = issue_stock(self.bank_teller_token, "浦发银行", '2021-3-20', 15)
        stock_id = response_dict['stock_id']

        buy_stock(self.bank_teller_token, self.customer_id, stock_id, 200, "2021-3-21")

        status_code, response_dict = issue_regular_deposit(self.bank_teller_token, "定期理财一号", '2021-3-20', 9, 0.07)
        regular_deposit_id = response_dict['regular_deposit_id']

        buy_regular_deposit(self.bank_teller_token, self.customer_id, regular_deposit_id, 100, "2021-3-21")

    def test_query_customer_fund_invest(self):
        # 正确查询基金投资情况测试
        status_code, response_dict = query_customer_fund_invest(self.bank_teller_token, self.customer_id, "2021-3-22")
        self.assertEqual(200, status_code)
        self.assertTrue(response_dict[0]["current_profit"])

        # 无柜员权限测试
        status_code, response_dict = query_customer_fund_invest('wrong token', self.customer_id, "2021-3-22")
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数缺失测试
        status_code, response_dict = query_customer_fund_invest(self.bank_teller_token, self.customer_id)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        status_code, response_dict = query_customer_fund_invest(self.bank_teller_token, self.customer_id, "2021-3-19")
        self.assertEqual(200, status_code)
        print(response_dict)
        # self.assertTrue(response_dict[0]["current_profit"])

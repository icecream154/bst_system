import os, django

from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from bts.bts_test.rpc_test import sys_register, sys_login, add_customer, customer_deposit, issue_fund, issue_stock, \
    issue_regular_deposit, buy_fund, buy_stock, buy_regular_deposit

from bts.models.constants import EM_INVALID_OR_MISSING_PARAMETERS

from django.test import Client


class TestInvestment(TestCase):
    def setUp(self):
        self.client = Client()
        sys_register("投资测试", "imbus123", "柜员", "13966667777")

        status_code, response_dict = sys_login("投资测试", "imbus123")
        self.bank_teller_token = response_dict['token']

        status_code, response_dict = add_customer(self.bank_teller_token, "客户一", "13100006789", "330888855590001",
                                                  1000.0)
        self.customer_id = response_dict["customer_id"]

        status_code, response_dict = issue_fund(self.bank_teller_token, "基金一号", '2021-3-20', 3.0)
        self.fund_id = response_dict['fund_id']

    def test_buy_fund(self):
        # 正确购买基金测试
        status_code, response_dict = buy_fund(self.bank_teller_token, self.customer_id, self.fund_id, 700, "2021-3-21",
                                              100)
        self.assertEqual(200, status_code)
        self.assertEqual("fund purchase success", response_dict['msg'])

        # 无柜员权限测试
        status_code, response_dict = buy_fund('wrong token', self.customer_id, self.fund_id, 700, "2021-3-21", 100)
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数缺失测试
        status_code, response_dict = buy_fund(self.bank_teller_token, self.customer_id, self.fund_id, 700, "2021-3-21")
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)
        #
        # # 参数错误测试
        # status_code, response_dict = customer_deposit(self.bank_teller_token, self.customer_id, -1000.0)
        # self.assertEqual(400, status_code)
        # self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)
        #
        # # 客户不存在测试
        # status_code, response_dict = customer_deposit(self.bank_teller_token, -1, 1000.0)
        # self.assertEqual(404, status_code)

import os, django

from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from bts.bts_test.rpc_test import sys_register, sys_login, add_customer, customer_deposit

from bts.models.constants import EM_INVALID_OR_MISSING_PARAMETERS

from django.test import Client


class TestDeposit(TestCase):
    def setUp(self):
        self.client = Client()
        sys_register("账户测试", "imbus123", "柜员", "13966667777")

        status_code, response_dict = sys_login("账户测试", "imbus123")
        self.bank_teller_token = response_dict['token']

        status_code, response_dict = add_customer(self.bank_teller_token, "客户一", "13100002345", "330888855560001",
                                                  1000.0)
        self.customer_id = response_dict["customer_id"]

    def test_customer_deposit(self):
        # 正确添加客户存款测试
        status_code, response_dict = customer_deposit(self.bank_teller_token, self.customer_id, 1000.0)
        self.assertEqual(200, status_code)
        self.assertEqual("customer deposit success", response_dict['msg'])

        # 无柜员权限测试
        status_code, response_dict = customer_deposit("wrong token", self.customer_id, 1000.0)
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数缺失测试
        status_code, response_dict = customer_deposit(self.bank_teller_token, self.customer_id)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 参数错误测试
        status_code, response_dict = customer_deposit(self.bank_teller_token, self.customer_id, -1000.0)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 客户不存在测试
        status_code, response_dict = customer_deposit(self.bank_teller_token, -1, 1000.0)
        self.assertEqual(404, status_code)

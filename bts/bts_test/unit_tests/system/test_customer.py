import os, django

from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from bts.bts_test.rpc_test import sys_register, sys_login, add_customer, query_customer_by_id_number

from bts.models.constants import EM_INVALID_OR_MISSING_PARAMETERS

from django.test import Client


class TestCustomer(TestCase):
    def setUp(self):
        self.client = Client()
        sys_register("客户测试", "imbus123", "柜员", "13966667777")

        status_code, response_dict = sys_login("客户测试", "imbus123")
        self.bank_teller_token = response_dict['token']

        self.id_number = "330888855550002"
        add_customer(self.bank_teller_token, "客户二", "13100001235", self.id_number, 1000.0)

    def test_add_customer(self):
        id_number = "330888855550001"
        # 正确添加客户测试
        status_code, response_dict = add_customer(self.bank_teller_token, "客户一", "13100001234", id_number, 1000.0)
        self.assertEqual(200, status_code)
        self.assertEqual("add new customer success", response_dict['msg'])

        # 无柜员权限测试
        status_code, response_dict = add_customer("wrong token", "客户一", "13100001234", id_number, 1000.0)
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数错误测试
        status_code, response_dict = add_customer(self.bank_teller_token, "客户一", "13100001234", id_number)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 身份证号重复测试
        status_code, response_dict = add_customer(self.bank_teller_token, "客户一", "13100001234", id_number, 1000.0)
        self.assertEqual(400, status_code)
        self.assertEqual("id number conflict", response_dict)

    def test_query_customer_by_id_number(self):
        # 正确查询测试
        status_code, response_dict = query_customer_by_id_number(self.bank_teller_token, self.id_number)
        self.assertEqual(200, status_code)
        self.assertEqual(self.id_number, response_dict["id_number"])

        # 无柜员权限测试
        status_code, response_dict = query_customer_by_id_number("wrong token", self.id_number)
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数错误测试
        status_code, response_dict = query_customer_by_id_number(self.bank_teller_token)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        status_code, response_dict = query_customer_by_id_number(self.bank_teller_token, "1")
        self.assertEqual(404, status_code)

import os, django

from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from bts.bts_test.rpc_test import sys_register, sys_login, add_customer, customer_loan, loan_query_record_by_id, \
    loan_query_record_by_customer_id

from bts.models.constants import EM_INVALID_OR_MISSING_PARAMETERS

from django.test import Client


class TestLoanQuery(TestCase):
    def setUp(self):
        self.client = Client()
        sys_register("借款查询测试", "imbus123", "柜员", "13966667777")

        status_code, response_dict = sys_login("借款查询测试", "imbus123")
        self.bank_teller_token = response_dict['token']

        status_code, response_dict = add_customer(self.bank_teller_token, "客户一", "13100004567", "330888855580001",
                                                  1000.0)
        self.customer_id = response_dict["customer_id"]

        status_code, response_dict = customer_loan(self.bank_teller_token, self.customer_id, 300, 30, '2021-3-20')
        self.loan_record_id = response_dict["loan_record_id"]

    def test_query_loan_record_by_id(self):
        # 正确查询测试
        status_code, response_dict = loan_query_record_by_id(self.bank_teller_token, self.loan_record_id)
        self.assertEqual(200, status_code)
        self.assertEqual(self.loan_record_id, response_dict['loan_record_id'])

        # 无柜员权限测试
        status_code, response_dict = loan_query_record_by_id("wrong token", self.loan_record_id)
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数缺失测试
        status_code, response_dict = loan_query_record_by_id(self.bank_teller_token, -1)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

    def test_query_loan_record_by_customer_id(self):
        # 正确查询测试
        status_code, response_dict = loan_query_record_by_customer_id(self.bank_teller_token, self.customer_id)
        self.assertEqual(200, status_code)
        self.assertEqual(1, len(response_dict))

        # 无柜员权限测试
        status_code, response_dict = loan_query_record_by_customer_id("wrong token", self.loan_record_id)
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数缺失测试
        status_code, response_dict = loan_query_record_by_customer_id(self.bank_teller_token, -1)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)
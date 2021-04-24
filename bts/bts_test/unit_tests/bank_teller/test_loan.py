import os, django

from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from bts.bts_test.rpc_test import sys_register, sys_login, add_customer, customer_loan, customer_loan_repay, \
    loan_auto_repay

from bts.models.constants import EM_INVALID_OR_MISSING_PARAMETERS

from django.test import Client


class TestLoan(TestCase):
    def setUp(self):
        self.client = Client()
        sys_register("借款测试", "imbus123", "柜员", "13966667777")

        status_code, response_dict = sys_login("借款测试", "imbus123")
        self.bank_teller_token = response_dict['token']

        status_code, response_dict = add_customer(self.bank_teller_token, "客户一", "13100003456", "330888855570001",
                                                  1000.0)
        self.customer_id = response_dict["customer_id"]

        status_code, response_dict = customer_loan(self.bank_teller_token, self.customer_id, 300, 30, '2021-3-20')
        self.loan_record_id = response_dict["loan_record_id"]

        # 未到期借款测试
        customer_loan(self.bank_teller_token, self.customer_id, 300, 300, '2021-3-20')

        # 账户余额不够归还本金测试
        customer_loan(self.bank_teller_token, self.customer_id, 3000, 30, '2021-3-20')

        status_code, response_dict = add_customer(self.bank_teller_token, "客户二", "13100003457", "330888855570002", 1.0)
        customer_id = response_dict["customer_id"]

        # 账户余额不够罚金测试
        customer_loan(self.bank_teller_token, customer_id, 300, 3, '2021-3-20')

    def test_request_loan(self):
        # 正确添加客户存款测试
        status_code, response_dict = customer_loan(self.bank_teller_token, self.customer_id, 300, 7, '2021-4-24')
        self.assertEqual(200, status_code)
        self.assertEqual("loan request success", response_dict['msg'])

        # 无柜员权限测试
        status_code, response_dict = customer_loan("wrong token", self.customer_id, 300, 7, '2021-4-24')
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数缺失测试
        status_code, response_dict = customer_loan(self.bank_teller_token, self.customer_id, 300, 7)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 参数错误测试（借款小于0）
        status_code, response_dict = customer_loan(self.bank_teller_token, self.customer_id, -300, 7, '2021-4-24')
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 客户不存在测试
        status_code, response_dict = customer_loan(self.bank_teller_token, -1, 300, 7, '2021-4-24')
        self.assertEqual(404, status_code)

    def test_loan_repay(self):
        # 正确还款测试1
        status_code, response_dict = customer_loan_repay(self.bank_teller_token, self.loan_record_id, 1)
        self.assertEqual(200, status_code)
        self.assertEqual("loan repay success", response_dict['msg'])

        # 正确还款测试2
        status_code, response_dict = customer_loan_repay(self.bank_teller_token, self.loan_record_id, 299)
        self.assertEqual(200, status_code)
        self.assertEqual("loan repay success", response_dict['msg'])

        # 无柜员权限测试
        status_code, response_dict = customer_loan_repay("wrong token", self.loan_record_id, 215)
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数缺失测试
        status_code, response_dict = customer_loan_repay(self.bank_teller_token, self.loan_record_id)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 参数错误测试（还款小于0）
        status_code, response_dict = customer_loan_repay(self.bank_teller_token, self.loan_record_id, -215)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 借款不存在测试
        status_code, response_dict = customer_loan_repay(self.bank_teller_token, -1, 215)
        self.assertEqual(404, status_code)

        # 还款过多测试
        status_code, response_dict = customer_loan_repay(self.bank_teller_token, self.loan_record_id, 100000)
        self.assertEqual(400, status_code)
        self.assertEqual("too much repay", response_dict)

    def test_auto_repay_process(self):
        # 正确自动还款测试
        status_code, response_dict = loan_auto_repay(self.bank_teller_token)
        self.assertEqual(200, status_code)
        self.assertEqual("auto repay process success", response_dict['msg'])

        # 无柜员权限测试
        status_code, response_dict = loan_auto_repay("wrong token")
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

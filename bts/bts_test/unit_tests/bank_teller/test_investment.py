import os, django

from django.test import TestCase

from bts.models.loan import LoanRecord

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from bts.bts_test.rpc_test import sys_register, sys_login, add_customer, customer_deposit, customer_loan, \
    loan_auto_repay, issue_fund, issue_stock, issue_regular_deposit, buy_fund, buy_stock, buy_regular_deposit, \
    get_customer_credit

from bts.services.bank_teller.loan import _calculate_fine

from bts.models.constants import EM_INVALID_OR_MISSING_PARAMETERS, EM_DEPOSIT_NOT_ENOUGH, EM_CANNOT_PAY_FINE

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

        status_code, response_dict = issue_stock(self.bank_teller_token, "浦发银行", '2021-3-20', 15)
        self.stock_id = response_dict['stock_id']

        status_code, response_dict = issue_regular_deposit(self.bank_teller_token, "定期理财一号", '2021-3-20', 9, 0.07)
        self.regular_deposit_id = response_dict['regular_deposit_id']

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

        # 客户不存在测试
        status_code, response_dict = buy_fund(self.bank_teller_token, -1, self.fund_id, 700, "2021-3-21", 100)
        self.assertEqual(404, status_code)

        # 基金不存在测试
        status_code, response_dict = buy_fund(self.bank_teller_token, self.customer_id, -1, 700, "2021-3-21", 100)
        self.assertEqual(404, status_code)

        # 余额不足测试
        status_code, response_dict = buy_fund(self.bank_teller_token, self.customer_id, self.fund_id, 70000,
                                              "2021-3-21", 100)
        self.assertEqual(403, status_code)
        self.assertEqual(EM_DEPOSIT_NOT_ENOUGH, response_dict)

        # 购买时间错误测试
        status_code, response_dict = buy_fund(self.bank_teller_token, self.customer_id, self.fund_id, 1, "2021-3-19",
                                              100)
        self.assertEqual(403, status_code)
        self.assertEqual("invalid purchase", response_dict)

        status_code, response_dict = customer_loan(self.bank_teller_token, self.customer_id, 300, 20, '2021-2-10')
        _calculate_fine(LoanRecord.objects.get(loan_record_id=response_dict['loan_record_id']))
        customer_loan(self.bank_teller_token, self.customer_id, 1, 20, '2021-2-10')

        # 信用等级不足测试
        status_code, response_dict = buy_fund(self.bank_teller_token, self.customer_id, self.fund_id, 1, "2021-3-21",
                                              100)
        self.assertEqual(403, status_code)
        self.assertEqual("credit level forbidden", response_dict)

        customer_loan(self.bank_teller_token, self.customer_id, 300000, 3, '2021-1-10')
        loan_auto_repay(self.bank_teller_token)

        # 余额无法还清罚款测试
        status_code, response_dict = buy_fund(self.bank_teller_token, self.customer_id, self.fund_id, 1, "2021-3-21",
                                              100)
        self.assertEqual(403, status_code)
        self.assertEqual(EM_CANNOT_PAY_FINE, response_dict)

    def test_buy_stock(self):
        # 信用等级不足测试
        status_code, response_dict = buy_stock(self.bank_teller_token, self.customer_id, self.stock_id, 20, "2021-3-21")
        self.assertEqual(403, status_code)
        self.assertEqual("credit level forbidden", response_dict)

        # 无柜员权限测试
        status_code, response_dict = buy_stock("wrong token", self.customer_id, self.stock_id, 20, "2021-3-21")
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数缺失测试
        status_code, response_dict = buy_stock(self.bank_teller_token, self.customer_id, self.stock_id, 20)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 客户不存在测试
        status_code, response_dict = buy_stock(self.bank_teller_token, -1, self.stock_id, 20, "2021-3-21")
        self.assertEqual(404, status_code)

        # 股票不存在测试
        status_code, response_dict = buy_stock(self.bank_teller_token, self.customer_id, -1, 20, "2021-3-21")
        self.assertEqual(404, status_code)

        # 购买时间错误测试
        status_code, response_dict = buy_stock(self.bank_teller_token, self.customer_id, self.stock_id, 20, "2021-3-19")
        self.assertEqual(403, status_code)
        self.assertEqual("invalid purchase", response_dict)

        # 余额不足测试
        status_code, response_dict = buy_stock(self.bank_teller_token, self.customer_id, self.stock_id, 2000,
                                               "2021-3-21")
        self.assertEqual(403, status_code)
        self.assertEqual(EM_DEPOSIT_NOT_ENOUGH, response_dict)

        customer_loan(self.bank_teller_token, self.customer_id, 30000, 1, '2021-1-10')
        loan_auto_repay(self.bank_teller_token)

        # 余额无法还清罚款测试
        status_code, response_dict = buy_stock(self.bank_teller_token, self.customer_id, self.stock_id, 1, "2021-3-21")
        self.assertEqual(403, status_code)
        self.assertEqual(EM_CANNOT_PAY_FINE, response_dict)

        customer_deposit(self.bank_teller_token, self.customer_id, 50000000)

        # 正确购买股票测试
        status_code, response_dict = buy_stock(self.bank_teller_token, self.customer_id, self.stock_id, 20, "2021-3-21")
        self.assertEqual(200, status_code)
        self.assertEqual("stock purchase success", response_dict["msg"])

        # 正确购买相同股票测试
        status_code, response_dict = buy_stock(self.bank_teller_token, self.customer_id, self.stock_id, 20, "2021-3-21")
        self.assertEqual(200, status_code)
        self.assertEqual("stock purchase success", response_dict["msg"])

    def test_buy_regular_deposit(self):
        # 正确购买定期理财测试
        status_code, response_dict = buy_regular_deposit(self.bank_teller_token, self.customer_id,
                                                         self.regular_deposit_id, 700, "2021-3-21")
        self.assertEqual(200, status_code)
        self.assertEqual("purchase success", response_dict['msg'])

        # 无柜员权限测试
        status_code, response_dict = buy_regular_deposit("wrong token", self.customer_id, self.regular_deposit_id, 700,
                                                         "2021-3-21")
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数缺失测试
        status_code, response_dict = buy_regular_deposit(self.bank_teller_token, self.customer_id,
                                                         self.regular_deposit_id, 700)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 客户不存在测试
        status_code, response_dict = buy_regular_deposit(self.bank_teller_token, -1, self.regular_deposit_id, 700,
                                                         "2021-3-21")
        self.assertEqual(404, status_code)

        # 定期理财不存在测试
        status_code, response_dict = buy_regular_deposit(self.bank_teller_token, self.customer_id, -1, 700, "2021-3-21")
        self.assertEqual(404, status_code)

        # 余额不足测试
        status_code, response_dict = buy_regular_deposit(self.bank_teller_token, self.customer_id,
                                                         self.regular_deposit_id, 70000, "2021-3-21")
        self.assertEqual(403, status_code)
        self.assertEqual(EM_DEPOSIT_NOT_ENOUGH, response_dict)

        customer_loan(self.bank_teller_token, self.customer_id, 30000, 1, '2021-1-10')
        loan_auto_repay(self.bank_teller_token)

        # 余额无法还清罚款测试
        status_code, response_dict = buy_regular_deposit(self.bank_teller_token, self.customer_id,
                                                         self.regular_deposit_id, 1, "2021-3-21")
        self.assertEqual(403, status_code)
        self.assertEqual(EM_CANNOT_PAY_FINE, response_dict)

    def test_get_customer_credit(self):
        # 正确查询信用等级测试
        status_code, response_dict = get_customer_credit(self.bank_teller_token, self.customer_id)
        self.assertEqual(200, status_code)
        self.assertTrue(response_dict['credit_level'])

        # 无柜员权限测试
        status_code, response_dict = get_customer_credit("wrong token", self.customer_id)
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数缺失测试
        status_code, response_dict = get_customer_credit(self.bank_teller_token)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 客户不存在测试
        status_code, response_dict = get_customer_credit(self.bank_teller_token, -1)
        self.assertEqual(404, status_code)

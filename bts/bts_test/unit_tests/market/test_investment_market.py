import os, django

from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from bts.bts_test.rpc_test import sys_register, sys_login, issue_fund, issue_stock, issue_regular_deposit, \
    get_fund_price, get_stock_price, query_funds, query_stocks, query_regular_deposits

from bts.models.constants import EM_INVALID_OR_MISSING_PARAMETERS, EM_PRODUCT_NAME_USED

from django.test import Client


class TestInvestmentMarket(TestCase):
    def setUp(self):
        self.client = Client()
        sys_register("投资市场测试", "imbus123", "柜员", "13966667777")

        status_code, response_dict = sys_login("投资市场测试", "imbus123")
        self.bank_teller_token = response_dict['token']

        status_code, response_dict = issue_fund(self.bank_teller_token, "基金二号", '2021-3-20', 3.2)
        self.fund_id = response_dict['fund_id']

        status_code, response_dict = issue_stock(self.bank_teller_token, "招商银行", '2021-3-30', 15)
        self.stock_id = response_dict['stock_id']

        status_code, response_dict = issue_regular_deposit(self.bank_teller_token, "定期理财二号", '2021-3-9', 9, 0.07)
        self.regular_deposit_id = response_dict['regular_deposit_id']

    def test_issue_fund(self):
        fund_name = "基金一号"
        # 正确发行基金测试
        status_code, response_dict = issue_fund(self.bank_teller_token, fund_name, '2021-3-20', 3.2)
        self.assertEqual(200, status_code)
        self.assertEqual("issue fund success", response_dict['msg'])

        # 无柜员权限测试
        status_code, response_dict = issue_fund("wrong token", fund_name, '2021-3-20', 3.2)
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数缺失测试
        status_code, response_dict = issue_fund(self.bank_teller_token, fund_name, '2021-3-20')
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 参数错误测试
        status_code, response_dict = issue_fund(self.bank_teller_token, fund_name, '2021-3-20', -1)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 基金重名测试
        status_code, response_dict = issue_fund(self.bank_teller_token, fund_name, '2021-3-20', 3.2)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_PRODUCT_NAME_USED, response_dict)

    def test_issue_stock(self):
        stock_name = "浦发银行"
        # 正确发行股票测试
        status_code, response_dict = issue_stock(self.bank_teller_token, stock_name, '2021-3-30', 15)
        self.assertEqual(200, status_code)
        self.assertEqual("issue stock success", response_dict['msg'])

        # 无柜员权限测试
        status_code, response_dict = issue_stock("wrong token", stock_name, '2021-3-30', 15)
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数缺失测试
        status_code, response_dict = issue_stock(self.bank_teller_token, stock_name, '2021-3-30')
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 参数错误测试
        status_code, response_dict = issue_stock(self.bank_teller_token, stock_name, '2021-3-30', -1)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 股票重名测试
        status_code, response_dict = issue_stock(self.bank_teller_token, stock_name, '2021-3-30', 15)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_PRODUCT_NAME_USED, response_dict)

    def test_issue_regular_deposit(self):
        regular_deposit_name = "定期理财一号"
        # 正确发行定期理财测试
        status_code, response_dict = issue_regular_deposit(self.bank_teller_token, regular_deposit_name, '2021-3-9', 9,
                                                           0.07)
        self.assertEqual(200, status_code)
        self.assertEqual("issue regular deposit success", response_dict['msg'])

        # 无柜员权限测试
        status_code, response_dict = issue_regular_deposit("wrong token", regular_deposit_name, '2021-3-9', 9, 0.07)
        self.assertEqual(401, status_code)
        self.assertEqual("Unauthorized", response_dict)

        # 参数缺失测试
        status_code, response_dict = issue_regular_deposit(self.bank_teller_token, regular_deposit_name, '2021-3-9', 9)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 参数错误测试
        status_code, response_dict = issue_regular_deposit(self.bank_teller_token, regular_deposit_name, '2021-3-9', 9,
                                                           -1)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 定期理财重名测试
        status_code, response_dict = issue_regular_deposit(self.bank_teller_token, regular_deposit_name, '2021-3-9', 9,
                                                           0.07)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_PRODUCT_NAME_USED, response_dict)

    def test_get_fund_price(self):
        # 正确查询基金价格测试
        status_code, response_dict = get_fund_price(self.fund_id, "2021-3-23")
        self.assertEqual(200, status_code)
        self.assertTrue(response_dict['price'])

        # 参数缺失测试
        status_code, response_dict = get_fund_price(self.fund_id)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 正确查询基金价格测试
        status_code, response_dict = get_fund_price(self.fund_id, "2021-3-15")
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

    def test_get_stock_price(self):
        # 正确查询股票价格测试
        status_code, response_dict = get_stock_price(self.stock_id, "2021-4-1")
        self.assertEqual(200, status_code)
        self.assertTrue(response_dict['price'])

        # 参数缺失测试
        status_code, response_dict = get_stock_price(self.stock_id)
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 正确查询基金价格测试
        status_code, response_dict = get_stock_price(self.stock_id, "2021-3-15")
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

    def test_query_funds(self):
        # 正确查询基金测试
        status_code, response_dict = query_funds(self.fund_id)
        self.assertEqual(200, status_code)
        self.assertEqual(self.fund_id, response_dict["fund_id"])

        # 参数缺失测试
        status_code, response_dict = query_funds()
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

    def test_query_stocks(self):
        # 正确查询股票测试
        status_code, response_dict = query_stocks(self.stock_id)
        self.assertEqual(200, status_code)
        self.assertEqual(self.fund_id, response_dict["stock_id"])

        # 参数缺失测试
        status_code, response_dict = query_stocks()
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

        # 所有股票正确查询测试
        status_code, response_dict = query_stocks(-1)
        self.assertEqual(200, status_code)
        self.assertEqual(1, len(response_dict))

    def test_query_regular_deposits(self):
        # 正确查询股票测试
        status_code, response_dict = query_regular_deposits(self.regular_deposit_id)
        self.assertEqual(200, status_code)
        self.assertEqual(self.fund_id, response_dict["regular_deposit_id"])

        # 定期理财不存在测试
        status_code, response_dict = query_regular_deposits(-2)
        self.assertEqual(404, status_code)

        # 参数缺失测试
        status_code, response_dict = query_regular_deposits()
        self.assertEqual(400, status_code)
        self.assertEqual(EM_INVALID_OR_MISSING_PARAMETERS, response_dict)

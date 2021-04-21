import unittest

from bts.bts_test.rpc_test import sys_register, sys_login


class TestLogin(unittest.TestCase):
    def setUp(self):
        sys_register('BTS1', 'imbus123', '柜员一', '13966667777')

    def test_login_success(self):
        # 柜员一登录，正确的用户名和正确的密码
        status_code, response_dict = sys_login('BTS1', 'imbus123')
        self.assertEqual(status_code, 200)
        self.assertTrue(response_dict['token'])

    def test_login_wrong_password(self):
        # 柜员一登录，正确的用户名和错误的密码
        status_code, response_dict = sys_login('BTS1', 'wrong-password')
        self.assertEqual(status_code, 403)

    def test_login_no_such_user(self):
        # 未注册的用户
        status_code, response_dict = sys_login('no-such-bank-teller', 'pass')
        self.assertEqual(status_code, 403)

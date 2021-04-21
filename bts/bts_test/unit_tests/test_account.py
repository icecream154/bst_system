from unittest import TestCase

from bts.bts_test.rpc_test import sys_register, sys_login


class TestAccount(TestCase):
    def test_bank_teller_register(self):
        status_code, response_dict = sys_register('BTS1', 'imbus123', '柜员一', '13966667777')
        self.assertEqual(200, status_code)

    def test_bank_teller_login(self):
        self.fail()

    def test_bank_teller_logout(self):
        self.fail()

import os, django

from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from bts.bts_test.rpc_test import sys_register, sys_login, sys_logout

from bts.services.system import token

import time

from django.test import Client


class TestAccount(TestCase):
    def setUp(self):
        self.client = Client()
        sys_register("登录测试", "imbus123", "柜员四", "13966667777")

    def test_bank_teller_register(self):
        # request = HttpRequest()
        # request.method = "POST"
        # request.META = {"CONTENT_TYPE": "application/json"}
        # request._body = json.dumps({"account": "BTS3", "password": "imbus123", "name": "柜员三", "phone": "13966667777"}).encode("UTF-8")
        # response = account.bank_teller_register(request)
        # status_code = response.status_code
        # response_dict = json.loads(response.content.decode("utf8"))

        # response = self.client.post('http://localhost:8000/bts/system/register',
        #                             data={"account": "BTS3", "password": "imbus123", "name": "柜员三",
        #                                   "phone": "13966667777"})

        # 正确注册测试
        status_code, response_dict = sys_register("注册测试", "imbus123", "柜员三", "13966667777")
        self.assertEqual(200, status_code)
        self.assertEqual("register bank teller success", response_dict["msg"])

        # 缺少参数注册测试
        status_code, response_dict = sys_register("注册测试", "imbus123", "柜员三")
        self.assertEqual(400, status_code)
        self.assertEqual("parameter missing or invalid parameter", response_dict)

        # 密码过于简单测试
        status_code, response_dict = sys_register("注册测试", "i", "柜员三", "13966667777")
        self.assertEqual(403, status_code)
        self.assertEqual("password not accepted, too simple", response_dict)

        # 账户已存在测试
        status_code, response_dict = sys_register("注册测试", "imbus123", "柜员三", "13966667777")
        self.assertEqual(403, status_code)
        self.assertEqual("account already exist", response_dict)

    def test_bank_teller_login(self):
        # 正确登录测试
        status_code, response_dict = sys_login("登录测试", "imbus123")
        self.assertEqual(200, status_code)
        self.assertTrue(response_dict['token'])

        # 缺少参数登录测试
        status_code, response_dict = sys_login("登录测试")
        self.assertEqual(400, status_code)
        self.assertEqual("parameter missing or invalid parameter", response_dict)

        # 用户不存在登录测试
        status_code, response_dict = sys_login("登录测试1", "imbus123")
        self.assertEqual(403, status_code)
        self.assertEqual("account doesn't exist", response_dict)

        # 密码错误登录测试
        status_code, response_dict = sys_login("登录测试", "imbus12")
        self.assertEqual(403, status_code)
        self.assertEqual("wrong password", response_dict)

    def test_bank_teller_logout(self):
        sys_login("登录测试", "imbus123")
        status_code, response_dict = sys_login("登录测试", "imbus123")

        # 正常登出测试
        user_token = response_dict['token']
        status_code, response_dict = sys_logout(user_token)
        self.assertEqual(200, status_code)
        self.assertEqual("logout success", response_dict["msg"])

        status_code, response_dict = sys_login("登录测试", "imbus123")

        # token过期测试
        user_token = response_dict['token']
        bank_teller = token.token_dict[user_token][0]
        token.token_dict[user_token] = (bank_teller, time.time() - 1)
        status_code, response_dict = sys_logout(user_token)
        self.assertEqual(403, status_code)
        self.assertEqual("invalid token", response_dict)

        # 无效token测试
        status_code, response_dict = sys_logout("wrong token")
        self.assertEqual(403, status_code)
        self.assertEqual("invalid token", response_dict)

        token.expire_token("wrong token")

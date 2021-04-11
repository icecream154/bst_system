from django.db import models


class BankTeller(models.Model):
    # 柜员ID
    bank_teller_id = models.AutoField(primary_key=True)
    # 登录账号
    account = models.CharField(max_length=20, unique=True)
    # 登录密码
    password = models.CharField(max_length=20)
    # 柜员姓名
    name = models.CharField(max_length=10)
    # 手机号
    phone = models.CharField(max_length=11)

    def __str__(self):
        return 'BankTeller [id: %d, account: %s, password: %s, name: %s]'\
               % (self.bank_teller_id, self.account, self.password, self.name)

from django.db import models

from bts.models.bank_teller import BankTeller


class Customer(models.Model):
    # 客户ID
    customer_id = models.AutoField(primary_key=True)
    # 客户姓名
    name = models.CharField(max_length=10)
    # 手机号
    phone = models.CharField(max_length=11)
    # 身份证号
    id_number = models.CharField(max_length=30, unique=True)
    # 账户余额
    deposit = models.FloatField()
    # 开户柜员
    bank_teller = models.ForeignKey(BankTeller, on_delete=models.CASCADE)

    def to_dict(self):
        dictionary = {
            'customer_id': self.customer_id,
            'name': self.name,
            'phone': self.phone,
            'id_number': self.id_number,
            'deposit': self.deposit,
            'bank_teller_id': self.bank_teller.bank_teller_id
        }
        return dictionary

from django.db import models
from bts.models.customer import Customer


class DepositRecord(models.Model):
    # 存款记录ID
    record_id = models.AutoField(primary_key=True)
    # 客户ID
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # 存款时间
    created_time = models.DateTimeField()
    # 存款金额
    payment = models.IntegerField()
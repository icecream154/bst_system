from django.db import models
from django.utils import timezone

from bts.models.constants import DATE_TIME_FORMAT
from bts.models.customer import Customer


class DepositRecord(models.Model):
    # 存款记录ID
    record_id = models.AutoField(primary_key=True)
    # 客户ID
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # 存款时间
    created_time = models.DateField(default=timezone.now)
    # 存款金额
    payment = models.FloatField()
    # 存款后账户余额
    current_deposit = models.FloatField()

    def to_dict(self):
        dictionary = {
            'record_id': self.record_id,
            'customer_id': self.customer.customer_id,
            'customer_id_number': self.customer.id_number,
            'created_time': self.created_time.strftime(DATE_TIME_FORMAT),
            'payment': self.payment,
            'current_deposit': self.current_deposit
        }
        return dictionary

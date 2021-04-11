from django.db import models
from django.utils import timezone

from bts.models.customer import Customer


class LoanRecord(models.Model):
    # 贷款记录ID
    loan_record_id = models.AutoField(primary_key=True)
    # 客户ID
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # 贷款金额
    payment = models.FloatField()
    # 还款周期(天数)
    repay_cycle = models.IntegerField()
    # 到期时间
    due_date = models.DateField()
    # 下一次逾期时间
    next_overdue_date = models.DateField()
    # 剩余还款金额
    left_payment = models.FloatField()
    # 剩余罚金
    left_fine = models.FloatField()
    # 贷款时间
    created_time = models.DateField(default=timezone.now)

    def to_dict(self):
        dictionary = {
            'loan_record_id': self.loan_record_id,
            'customer_id': self.customer.customer_id,
            'created_time': self.created_time.strftime('%Y-%m-%d'),
            'payment': self.payment,
            'repay_cycle': self.repay_cycle,
            'due_date': self.due_date.strftime('%Y-%m-%d'),
            'next_overdue_date': self.next_overdue_date.strftime('%Y-%m-%d'),
            'left_payment': self.left_payment,
            'left_fine': self.left_fine,
        }
        return dictionary


class LoanRepay(models.Model):
    # 贷款还款记录ID
    repay_id = models.AutoField(primary_key=True)
    # 对应贷款记录
    loan_record = models.ForeignKey(LoanRecord, on_delete=models.CASCADE)
    # 还款前剩余还款金额
    left_payment_before = models.FloatField()
    # 还款前剩余罚金
    left_fine_before = models.FloatField()
    # 当前还款金额
    repay = models.FloatField()
    # 还款时间
    repay_time = models.DateField(default=timezone.now)

    def to_dict(self):
        dictionary = {
            'repay_id': self.repay_id,
            'loan_record_id': self.loan_record.loan_record_id,
            'left_payment_before': self.left_payment_before,
            'left_fine_before': self.left_fine_before,
            'repay': self.repay,
            'repay_time': self.repay_time.strftime('%Y-%m-%d'),
        }
        return dictionary
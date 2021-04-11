from django.db import models
from django.utils import timezone

from bts.models.products import Fund, Stock, RegularDeposit
from bts.models.customer import Customer


class FundInvestment(models.Model):
    """
    用户当前的基金买入情况
    """
    # 客户ID
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # 基金ID
    fund_id = models.ForeignKey(Fund, on_delete=models.CASCADE)
    # 持仓份额
    position_share = models.FloatField()
    # 累计买入金额
    cumulative_purchase_amount = models.FloatField()
    # 最早买入时间
    purchase_date = models.DateTimeField(default=timezone.now)

    def to_dict(self):
        dictionary = {
            'customer_id': self.customer_id,
            'fund_id': self.fund_id,
            'position_share': self.position_share,
            'cumulative_purchase_amount': self.cumulative_purchase_amount,
            'purchase_date': self.purchase_date
        }
        return dictionary


class StockInvestment(models.Model):
    """
    用户当前的股票买入情况
    """
    # 客户ID
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # 股票ID
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    # 持仓股数(股数只能是整数)
    position_share = models.IntegerField()
    # 累计买入金额
    cumulative_purchase_amount = models.FloatField()
    # 最早买入时间
    purchase_date = models.DateTimeField(default=timezone.now)

    def to_dict(self):
        dictionary = {
            'customer_id': self.customer_id,
            'stock_id': self.stock_id,
            'position_share': self.position_share,
            'cumulative_purchase_amount': self.cumulative_purchase_amount,
            'purchase_date': self.purchase_date
        }
        return dictionary


class RegularDepositInvestment(models.Model):
    """
    用户当前的定期理财产品买入情况
    """
    # 客户ID
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # 定期理财产品Id
    regular_deposit_id = models.ForeignKey(RegularDeposit, on_delete=models.CASCADE)
    # 买入金额
    purchase_amount = models.FloatField()
    # 买入时间
    purchase_date = models.DateTimeField(default=timezone.now)
    # 到期时间
    due_date = models.DateField()

    def to_dict(self):
        dictionary = {
            'customer_id': self.customer_id,
            'regular_deposit_id': self.regular_deposit_id,
            'purchase_amount': self.purchase_amount,
            'purchase_date': self.purchase_date,
            'due_date': self.due_date
        }
        return dictionary

# TODO: 理财产品买卖记录

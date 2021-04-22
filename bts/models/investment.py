from django.db import models
from django.utils import timezone

from bts.models.constants import DATE_TIME_FORMAT
from bts.models.products import Fund, Stock, RegularDeposit
from bts.models.customer import Customer


class FundInvestment(models.Model):
    """
    用户当前的基金买入情况
    """
    # 所属客户
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # 所属基金
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    # 持仓份额
    position_share = models.FloatField()
    # 累计买入金额
    purchase_amount = models.FloatField()
    # 买入时间
    purchase_date = models.DateField(default=timezone.now)
    # 到期时间
    due_date = models.DateField()
    # 买入后账户余额
    current_deposit = models.FloatField()

    def to_dict(self):
        dictionary = {
            'customer_id': self.customer.customer_id,
            'fund_id': self.fund.fund_id,
            'position_share': self.position_share,
            'purchase_amount': self.purchase_amount,
            'purchase_date': self.purchase_date.strftime(DATE_TIME_FORMAT),
            'due_date': self.due_date.strftime(DATE_TIME_FORMAT),
            'current_deposit': self.current_deposit,
        }
        return dictionary


class StockInvestment(models.Model):
    """
    用户当前的股票买入情况
    """
    # 所属客户
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # 所属股票
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    # 持仓股数(股数只能是整数)
    position_share = models.IntegerField()
    # 累计买入金额
    cumulative_purchase_amount = models.FloatField()
    # 最早买入时间
    purchase_date = models.DateField(default=timezone.now)
    # 最近一次买入后账户余额
    current_deposit = models.FloatField()

    def to_dict(self):
        dictionary = {
            'customer_id': self.customer.customer_id,
            'stock_id': self.stock.stock_id,
            'position_share': self.position_share,
            'cumulative_purchase_amount': self.cumulative_purchase_amount,
            'purchase_date': self.purchase_date.strftime(DATE_TIME_FORMAT),
            'current_deposit': self.current_deposit,
        }
        return dictionary


class StockInvestmentRecord(models.Model):
    """
    用户历史股票买入情况
    """
    # 所属客户
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # 所属股票
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    # 买入股数(股数只能是整数)
    position_share = models.IntegerField()
    # 买入金额 （买入金额应该为买入时间的股票价格乘以股数）
    purchase_amount = models.FloatField()
    # 买入时间
    purchase_date = models.DateField(default=timezone.now)
    # 买入后账户余额
    current_deposit = models.FloatField()

    def to_dict(self):
        dictionary = {
            'customer_id': self.customer.customer_id,
            'stock_id': self.stock.stock_id,
            'position_share': self.position_share,
            'purchase_amount': self.purchase_amount,
            'purchase_date': self.purchase_date.strftime(DATE_TIME_FORMAT),
            'current_deposit': self.current_deposit,
        }
        return dictionary


class RegularDepositInvestment(models.Model):
    """
    用户当前的定期理财产品买入情况
    """
    # 客户ID
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # 定期理财产品Id
    regular_deposit = models.ForeignKey(RegularDeposit, on_delete=models.CASCADE)
    # 买入金额
    purchase_amount = models.FloatField()
    # 买入时间
    purchase_date = models.DateField(default=timezone.now)
    # 到期时间
    due_date = models.DateField()
    # 买入后账户余额
    current_deposit = models.FloatField()

    def to_dict(self):
        dictionary = {
            'customer_id': self.customer.customer_id,
            'regular_deposit_id': self.regular_deposit.regular_deposit_id,
            'purchase_amount': self.purchase_amount,
            'purchase_date': self.purchase_date.strftime(DATE_TIME_FORMAT),
            'due_date': self.due_date.strftime(DATE_TIME_FORMAT),
            'current_deposit': self.current_deposit,
        }
        return dictionary

# TODO: 理财产品买卖记录

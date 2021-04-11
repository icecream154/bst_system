import django.utils.timezone as timezone
from django.db import models


class Fund(models.Model):
    # 基金ID
    fund_id = models.AutoField(primary_key=True)
    # 基金名称
    fund_name = models.CharField(max_length=10, unique=True)
    # 发行日期
    issue_date = models.DateField(default=timezone.now)
    # 发型价格
    issue_price = models.FloatField()

    def to_dict(self):
        dictionary = {
            'fund_id': self.fund_id,
            'fund_name': self.fund_name,
            'issue_date': self.issue_date,
            'issue_price': self.issue_price
        }
        return dictionary


class Stock(models.Model):
    # 股票ID
    stock_id = models.AutoField(primary_key=True)
    # 股票名称
    stock_name = models.CharField(max_length=10, unique=True)
    # 发行日期
    issue_date = models.DateField(default=timezone.now)
    # 发型价格
    issue_price = models.FloatField()

    def to_dict(self):
        dictionary = {
            'stock_id': self.stock_id,
            'stock_name': self.stock_name,
            'issue_date': self.issue_date,
            'issue_price': self.issue_price
        }
        return dictionary


class RegularDeposit(models.Model):
    # 定期理财产品Id
    regular_deposit_id = models.AutoField(primary_key=True)
    # 定期理财产品名称
    regular_deposit_name = models.CharField(max_length=10, unique=True)
    # 发行日期
    issue_date = models.DateField(default=timezone.now)
    # 返还周期(天)
    return_cycle = models.IntegerField()
    # 利率
    return_rate = models.FloatField()

    def to_dict(self):
        dictionary = {
            'regular_deposit_id': self.regular_deposit_id,
            'regular_deposit_name': self.regular_deposit_name,
            'issue_date': self.issue_date,
            'return_cycle': self.return_cycle,
            'return_rate': self.return_rate
        }
        return dictionary


class FundPriceRecord(models.Model):
    fund_id = models.ForeignKey(Fund, on_delete=models.CASCADE)
    record_date = models.DateField()
    price = models.FloatField()


class StockPriceRecord(models.Model):
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    record_date = models.DateField()
    price = models.FloatField()

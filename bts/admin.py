from django.contrib import admin

# Register your models here.
from bts.models.bank_teller import BankTeller
from bts.models.customer import Customer
from bts.models.deposit import DepositRecord
from bts.models.loan import LoanRecord, LoanRepay
from bts.models.products import Fund, Stock, RegularDeposit, FundPriceRecord, StockPriceRecord
from bts.models.investment import FundInvestment, StockInvestment, RegularDepositInvestment

admin.site.register(BankTeller)

admin.site.register(Customer)

admin.site.register(DepositRecord)

admin.site.register(LoanRecord)
admin.site.register(LoanRepay)

admin.site.register(Fund)
admin.site.register(Stock)
admin.site.register(RegularDeposit)
admin.site.register(FundPriceRecord)
admin.site.register(StockPriceRecord)

admin.site.register(FundInvestment)
admin.site.register(StockInvestment)
admin.site.register(RegularDepositInvestment)

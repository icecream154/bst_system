from django.urls import path

from . import views
from .services.system import account, customer
from .services.bank_teller import deposit, loan_query
from .services.bank_teller import loan
from .services.bank_teller import investment, investment_query
from .services.market import investment_market
from .services.record_query import deposit, repay

urlpatterns = [
    path('', views.index, name='index'),
    # --系统模块--
    # 柜员注册
    path('system/register', account.bank_teller_register, name='register'),
    # 登录
    path('system/login', account.bank_teller_login, name='login'),
    # 登出
    path('system/logout', account.bank_teller_logout, name='logout'),

    # --客户模块--
    # 添加新客户
    path('customer/add', customer.add_customer, name='add_customer'),
    # 通过身份证号查询客户
    path('customer/query_by_id_number', customer.query_customer_by_id_number,
         name='query_customer_by_id_number'),

    # --存款模块--
    # 客户存款
    path('deposit', deposit.customer_deposit, name='deposit'),

    # --贷款模块--
    # 客户贷款
    path('loan/request_loan', loan.request_loan, name='request_loan'),
    # 通过贷款记录ID查询贷款
    path('loan/query_by_record_id', loan_query.query_loan_record_by_id, name='query_loan_record_by_id'),
    # 通过客户ID查询客户贷款记录
    path('loan/query_by_customer_id', loan_query.query_loan_record_by_customer_id,
         name='query_loan_record_by_customer_id'),
    # 贷款还款
    path('loan/repay', loan.loan_repay, name='loan_repay'),
    # 日终处理
    path('loan/auto_repay', loan.auto_repay_process, name='auto_repay'),

    # --投资模块--
    # 获取客户账户等级
    path('investment/get_customer_credit', investment.get_customer_credit, name='get_credit'),
    # 买入定期理财
    path('investment/buy_regular_deposit', investment.buy_regular_deposit, name='buy_regular_deposit'),
    # 买入基金
    path('investment/buy_fund', investment.buy_fund, name='buy_fund'),
    # 买入股票
    path('investment/buy_stock', investment.buy_stock, name='buy_stock'),

    # 查询客户买入的定期理财
    path('investment/query_customer_regular_deposit_invest', investment_query.query_customer_regular_deposit_invest,
         name='query_customer_regular_deposit_invest'),
    # 查询客户买入的基金
    path('investment/query_customer_fund_invest', investment_query.query_customer_fund_invest,
         name='query_customer_fund_invest'),
    # 查询客户买入的股票
    path('investment/query_customer_stock_invest', investment_query.query_customer_stock_invest,
         name='query_customer_stock_invest'),

    # --市场模块--
    # 基金查询
    path('market/query_funds', investment_market.query_funds, name='query_funds'),
    # 股票查询
    path('market/query_stocks', investment_market.query_stocks, name='query_stocks'),
    # 定期理财查询
    path('market/query_regular_deposits', investment_market.query_regular_deposits, name='query_regular_deposits'),

    # 获取基金当前价格
    path('market/get_fund_price', investment_market.get_fund_price, name='get_fund_price'),
    # 获取股票当前价格
    path('market/get_stock_price', investment_market.get_stock_price, name='get_stock_price'),

    # 发行基金
    path('market/issue_fund', investment_market.issue_fund, name='issue_fund'),
    # 发行股票
    path('market/issue_stock', investment_market.issue_stock, name='issue_stock'),
    # 发行定期理财产品
    path('market/issue_regular_deposit', investment_market.issue_regular_deposit, name='issue_regular_deposit'),

    # 流水模块
    # 查询存款记录
    path('record_query/deposit', deposit.query_deposits_by_customer_id, name='query_deposits_by_customer_id'),
    # 查询还款记录
    path('record_query/repay', repay.query_repays_by_customer_id, name='query_repays_by_customer_id'),
]

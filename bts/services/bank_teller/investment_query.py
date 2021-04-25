import json
from datetime import datetime, date

from django.db.models import Sum
from django.http import HttpResponse, HttpResponseBadRequest

from bts.models.constants import DATE_TIME_FORMAT, EM_INVALID_OR_MISSING_PARAMETERS
from bts.models.customer import Customer
from bts.models.investment import FundInvestment, StockInvestment, RegularDepositInvestment, StockInvestmentRecord
from bts.models.products import RegularDeposit, Fund, Stock
from bts.services.market.investment_market import get_fund_price_from_market, get_stock_price_from_market
from bts.services.system.token import fetch_bank_teller_by_token, TOKEN_HEADER_KEY


def query_customer_fund_invest(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer = Customer.objects.get(customer_id=int(request.GET['customer_id']))
        query_date = datetime.strptime(request.GET['query_date'], DATE_TIME_FORMAT).date()
    except (KeyError, ValueError, TypeError, Customer.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    fund_invest_list = _query_customer_product_invest(customer, FundInvestment)
    fund_invest_dict_list = []
    for fund_invest in fund_invest_list:
        curr_fund_price = get_fund_price_from_market(fund=fund_invest.fund, search_date=query_date)
        fund_invest_dict = fund_invest.to_dict()
        fund_invest_dict['current_profit'] = None
        if curr_fund_price and query_date >= fund_invest.purchase_date:
            fund_invest['current_profit'] = fund_invest['position_share'] * curr_fund_price \
                                            - fund_invest['purchase_amount']
        fund_invest_dict_list.append(fund_invest_dict)
    return HttpResponse(json.dumps(fund_invest_dict_list))


def query_customer_stock_invest(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer = Customer.objects.get(customer_id=int(request.GET['customer_id']))
        query_date = datetime.strptime(request.GET['query_date'], DATE_TIME_FORMAT).date()
    except (KeyError, ValueError, TypeError, Customer.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    stock_invest_list = _query_customer_product_invest(customer, StockInvestment)
    stock_invest_dict_list = []
    for stock_invest in stock_invest_list:
        curr_stock_price = get_stock_price_from_market(stock=stock_invest.stock, search_date=query_date)
        stock_invest_dict = stock_invest.to_dict()
        stock_invest_dict['current_profit'] = None
        total_position_share, cumulative_purchase_amount = \
            _get_position_share_and_cumulative_purchase_amount(customer, stock_invest.stock, query_date)
        if curr_stock_price and query_date >= stock_invest.purchase_date:
            stock_invest['current_profit'] = total_position_share * curr_stock_price \
                                             - cumulative_purchase_amount
        stock_invest_dict_list.append(stock_invest_dict)
    return HttpResponse(json.dumps(stock_invest_dict_list))


def _get_position_share_and_cumulative_purchase_amount(customer: Customer, stock: Stock, query_date: date):
    stock_invest_records = StockInvestmentRecord.objects.filter(customer=customer, stock=stock,
                                                                purchase_date__lte=query_date)
    total_position_share = stock_invest_records.aggregate(
        total_position_share=Sum('position_share'))['total_position_share']
    cumulative_purchase_amount = stock_invest_records.aggregate(
        cumulative_purchase_amount=Sum('purchase_amount'))['cumulative_purchase_amount']
    return total_position_share, cumulative_purchase_amount


def query_customer_regular_deposit_invest(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer = Customer.objects.get(customer_id=int(request.GET['customer_id']))
    except (KeyError, ValueError, TypeError, Customer.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    regular_deposit_invest_list = _query_customer_product_invest(customer, RegularDepositInvestment)
    regular_deposit_invest_dict_list = []
    for regular_deposit_invest in regular_deposit_invest_list:
        return_rate = regular_deposit_invest.return_rate
        regular_deposit_invest_dict = regular_deposit_invest.to_dict()
        regular_deposit_invest_dict['expecting_profit'] = return_rate * regular_deposit_invest.purchase_amount
        regular_deposit_invest_dict_list.append(regular_deposit_invest_dict)
    return HttpResponse(json.dumps(regular_deposit_invest_dict_list))


def _query_customer_product_invest(customer: Customer, product_invest_cls):
    return list(product_invest_cls.objects.filter(customer=customer))

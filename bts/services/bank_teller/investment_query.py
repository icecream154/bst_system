import json
from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest

from bts.models.constants import DATE_TIME_FORMAT, EM_INVALID_OR_MISSING_PARAMETERS
from bts.models.customer import Customer
from bts.models.investment import FundInvestment, StockInvestment, RegularDepositInvestment
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
    for fund_invest in fund_invest_list:
        fund = Fund.objects.get(fund_id=fund_invest['fund_id'])
        curr_fund_price = get_fund_price_from_market(fund=fund, search_date=query_date)
        fund_invest['current_profit'] = None
        if curr_fund_price and query_date >= fund_invest.purchase_date:
            fund_invest['current_profit'] = fund_invest['position_share'] * curr_fund_price \
                                            - fund_invest['purchase_amount']

    return HttpResponse(json.dumps(fund_invest_list))


def query_customer_stock_invest(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer = Customer.objects.get(customer_id=int(request.GET['customer_id']))
        query_date = datetime.strptime(request.GET['query_date'], DATE_TIME_FORMAT).date()
    except (KeyError, ValueError, TypeError, Customer.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    stock_invest_list = _query_customer_product_invest(customer, StockInvestment)
    for stock_invest in stock_invest_list:
        stock = Stock.objects.get(stock_id=stock_invest['stock_id'])
        curr_stock_price = get_stock_price_from_market(stock=stock, search_date=query_date)
        stock_invest['current_profit'] = None
        if curr_stock_price and query_date >= stock_invest.purchase_date:
            stock_invest['current_profit'] = stock_invest['position_share'] * curr_stock_price \
                                             - stock_invest['cumulative_purchase_amount']
    return HttpResponse(json.dumps(stock_invest_list))


def query_customer_regular_deposit_invest(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer = Customer.objects.get(customer_id=int(request.GET['customer_id']))
    except (KeyError, ValueError, TypeError, Customer.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    regular_deposit_invest_list = _query_customer_product_invest(customer, RegularDepositInvestment)
    for regular_deposit_invest in regular_deposit_invest_list:
        return_rate = RegularDeposit.objects.get(regular_deposit_id=regular_deposit_invest['regular_deposit_id']) \
            .return_rate
        regular_deposit_invest['expecting_profit'] = return_rate * regular_deposit_invest['purchase_amount']
    return HttpResponse(json.dumps(regular_deposit_invest_list))


def _query_customer_product_invest(customer: Customer, product_invest_cls):
    product_invest_obj_list = list(product_invest_cls.objects.filter(customer=customer))
    # TODO: 不用转dict
    product_invest_list = []
    for product_invest in product_invest_obj_list:
        product_invest_list.append(product_invest.to_dict())
    return product_invest_list

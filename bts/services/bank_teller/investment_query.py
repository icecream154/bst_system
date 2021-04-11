import json
from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest

from bts.models.investment import FundInvestment, StockInvestment, RegularDepositInvestment
from bts.models.products import RegularDeposit
from bts.services.market.investment_market import _get_fund_price, _get_stock_price
from bts.services.system.token import fetch_bank_teller_by_token


def query_customer_fund_invest(request):
    if not fetch_bank_teller_by_token(request.META['token']):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer_id = int(request.GET['customer_id'])
        query_date = datetime.strptime(request.GET['query_date'], '%Y-%m-%d')
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')

    fund_invest_list = _query_customer_product_invest(customer_id, FundInvestment)
    for fund_invest in fund_invest_list:
        curr_fund_price = _get_fund_price(fund_id=fund_invest['fund_id'], search_date=query_date)
        if curr_fund_price:
            fund_invest['current_profit'] = fund_invest['position_share'] * curr_fund_price \
                                            - fund_invest['purchase_amount']
        else:
            fund_invest['current_profit'] = None
    return HttpResponse(json.dumps(fund_invest_list))


def query_customer_stock_invest(request):
    if not fetch_bank_teller_by_token(request.META['token']):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer_id = int(request.GET['customer_id'])
        query_date = datetime.strptime(request.GET['query_date'], '%Y-%m-%d')
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')

    stock_invest_list = _query_customer_product_invest(customer_id, StockInvestment)
    for stock_invest in stock_invest_list:
        curr_stock_price = _get_stock_price(stock_id=stock_invest['stock_id'], search_date=query_date)
        if curr_stock_price:
            stock_invest['current_profit'] = stock_invest['position_share'] * curr_stock_price \
                                            - stock_invest['cumulative_purchase_amount']
        else:
            stock_invest['current_profit'] = None
    return HttpResponse(json.dumps(stock_invest_list))


def query_customer_regular_deposit_invest(request):
    if not fetch_bank_teller_by_token(request.META['token']):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer_id = int(request.GET['customer_id'])
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')

    regular_deposit_invest_list = _query_customer_product_invest(customer_id, RegularDepositInvestment)
    for regular_deposit_invest in regular_deposit_invest_list:
        return_rate = RegularDeposit.objects.get(regular_deposit_id=regular_deposit_invest['regular_deposit_id'])\
                        .return_rate
        regular_deposit_invest['expecting_profit': return_rate * regular_deposit_invest['purchase_amount']]
    return HttpResponse(json.dumps(regular_deposit_invest_list))


def _query_customer_product_invest(customer_id: int, product_invest_cls):
    product_invest_obj_list = list(product_invest_cls.objects.filter(customer_id=customer_id))
    product_invest_list = []
    for product_invest in product_invest_obj_list:
        product_invest_list.add(product_invest.to_dict())
    return product_invest_list

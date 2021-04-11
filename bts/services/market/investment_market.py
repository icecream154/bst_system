import json
import random
from datetime import timedelta, datetime

from django.http import HttpResponseBadRequest, HttpResponse, Http404

from bts.models.products import FundPriceRecord, StockPriceRecord, Fund, Stock, RegularDeposit
from bts.services.system.token import fetch_bank_teller_by_token, TOKEN_HEADER_KEY


def _query_products(query_id: int, product_cls):
    if query_id == -1:
        product_list = list(product_cls.objects.all())
        response_data = []
        for product in product_list:
            response_data.add(product.to_dict())
        return HttpResponse(json.dumps(response_data))
    try:
        product = product_cls.objects.get(pk=query_id)
        return HttpResponse(json.dumps(product.to_dict()))
    except product_cls.DoesNotExist:
        raise Http404('No such product')


def query_funds(request):
    try:
        fund_id = int(request.GET['product_id'])
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')
    return _query_products(fund_id, Fund)


def query_stocks(request):
    try:
        stock_id = int(request.GET['product_id'])
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')
    return _query_products(stock_id, Stock)


def query_regular_deposits(request):
    try:
        regular_deposit_id = int(request.GET['product_id'])
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')
    return _query_products(regular_deposit_id, RegularDeposit)


def _get_random_fluctuation(fluctuation_range: float = 0.05):
    return (random.random() - 0.5) * 2 * fluctuation_range


def _get_fund_price(fund_id: int, search_date):
    try:
        if Fund.objects.get(fund_id=fund_id).issue_date <= search_date:
            price_record = FundPriceRecord.objects.get(fund_id=fund_id, record_date=search_date)
            return price_record.price
        else:
            return None
    except Fund.DoesNotExist:
        return None
    except FundPriceRecord.DoesNotExist:
        last_price = _get_fund_price(fund_id, search_date - timedelta(days=1))
        price = last_price * _get_random_fluctuation()
        FundPriceRecord(fund_id=fund_id, record_date=search_date,
                        price=price).save()
        return price


def _get_stock_price(stock_id: int, search_date):
    try:
        if Stock.objects.get(stock_id=stock_id).issue_date <= search_date:
            price_record = StockPriceRecord.objects.get(stock_id=stock_id, record_date=search_date)
            return price_record.price
        else:
            return None
    except Stock.DoesNotExist:
        return None
    except StockPriceRecord.DoesNotExist:
        last_price = _get_stock_price(stock_id, search_date - timedelta(days=1))
        price = last_price * _get_random_fluctuation(0.1)
        StockPriceRecord(stock_id=stock_id, record_date=search_date,
                         price=price).save()
        return price


def get_fund_price(request):
    try:
        fund_id = int(request.GET['fund_id'])
        search_date = datetime.strptime(request.GET['search_date'], '%Y-%m-%d')
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')
    except Exception as ex:
        print(ex)
        return HttpResponseBadRequest('invalid parameter')

    response_data = {'price': _get_fund_price(fund_id, search_date)}
    if not response_data['price']:
        return HttpResponseBadRequest('invalid parameter')
    return HttpResponse(json.dumps(response_data))


def get_stock_price(request):
    try:
        stock_id = int(request.GET['stock_id'])
        search_date = datetime.strptime(request.GET['search_date'], '%Y-%m-%d')
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')
    except Exception as ex:
        print(ex)
        return HttpResponseBadRequest('invalid parameter')

    response_data = {'price': _get_stock_price(stock_id, search_date)}
    if not response_data['price']:
        return HttpResponseBadRequest('invalid parameter')
    return HttpResponse(json.dumps(response_data))


def issue_fund(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)
    try:
        fund_name = request.POST['fund_name']
        issue_date = datetime.strptime(request.POST['issue_date'], '%Y-%m-%d')
        issue_price = float(request.POST['issue_price'])
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')
    if issue_price <= 0:
        return HttpResponseBadRequest('invalid parameter')
    new_fund = Fund(fund_name=fund_name, issue_date=issue_date, issue_price=issue_price)
    new_fund.save()
    FundPriceRecord(fund_id=new_fund.fund_id, record_date=issue_date, price=issue_price).save()
    response_data = {'msg': 'issue fund success', 'fund_id': new_fund.fund_id}
    return HttpResponse(json.dumps(response_data))


def issue_stock(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)
    try:
        stock_name = request.POST['stock_name']
        issue_date = datetime.strptime(request.POST['issue_date'], '%Y-%m-%d')
        issue_price = float(request.POST['issue_price'])
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')
    if issue_price <= 0:
        return HttpResponseBadRequest('invalid parameter')
    new_stock = Stock(stock_name=stock_name, issue_date=issue_date, issue_price=issue_price)
    new_stock.save()
    StockPriceRecord(stock_id=new_stock.stock_id, record_date=issue_date, price=issue_price).save()
    response_data = {'msg': 'issue stock success', 'stock_id': new_stock.stock_id}
    return HttpResponse(json.dumps(response_data))


def issue_regular_deposit(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)
    try:
        regular_deposit_name = request.POST['regular_deposit_name']
        issue_date = datetime.strptime(request.POST['issue_date'], '%Y-%m-%d')
        return_cycle = int(request.POST['return_cycle'])
        return_rate = float(request.POST['return_rate'])
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')
    if return_rate <= 0 or return_rate > 0.2 or return_cycle < 7:
        return HttpResponseBadRequest('invalid parameter')
    new_regular_deposit = RegularDeposit(regular_deposit_name=regular_deposit_name,
                                         issue_date=issue_date,
                                         return_cycle=return_cycle,
                                         return_rate=return_rate)
    new_regular_deposit.save()
    response_data = {'msg': 'issue regular deposit success',
                     'regular_deposit_id': new_regular_deposit.regular_deposit_id}
    return HttpResponse(json.dumps(response_data))

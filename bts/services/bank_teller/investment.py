import json
from datetime import datetime, timedelta

from django.db.models import aggregates, Sum
from django.http import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseForbidden

from bts.models.customer import Customer
from bts.models.investment import RegularDepositInvestment, FundInvestment, StockInvestment
from bts.models.loan import LoanRecord
from bts.models.products import RegularDeposit, Fund, Stock
from bts.services.bank_teller.loan import _loan_repay
from bts.services.market.investment_market import _get_fund_price, _get_stock_price
from bts.services.system.token import fetch_bank_teller_by_token, TOKEN_HEADER_KEY


class Credit:
    Credit_Primary_Account = 1  # 一级账户
    Credit_Secondary_Account = 2  # 二级账户
    Credit_Third_Level_Account = 3  # 三级账户

    Credit_Primary_Account_Limit = 500000.0
    Credit_Secondary_Account_Limit = 0


def _get_customer_credit(customer: Customer):
    total_left_payment = LoanRecord.objects.filter(customer_id=customer.customer_id) \
        .aggregates(total_left_payment=Sum('left_payment'))['total_left_payment']
    total_left_fine = LoanRecord.objects.filter(customer_id=customer.customer_id) \
        .aggregates(total_left_fine=Sum('left_fine'))['total_left_fine']

    credit_info = {
        'deposit': customer.deposit,
        'total_left_payment': total_left_payment,
        'total_left_fine': total_left_fine,
        'net_capital': customer.deposit - total_left_payment - total_left_fine
    }
    if credit_info['net_capital'] > Credit.Credit_Primary_Account_Limit:
        credit_info['credit_level'] = Credit.Credit_Primary_Account
    elif credit_info['net_capital'] > Credit.Credit_Secondary_Account_Limit:
        credit_info['credit_level'] = Credit.Credit_Secondary_Account
    else:
        credit_info['credit_level'] = Credit.Credit_Third_Level_Account

    return credit_info


def get_customer_credit(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer_id = int(request.GET['customer_id'])
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')

    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        raise Http404('No such customer')

    return HttpResponse(json.dumps(_get_customer_credit(customer)))


def _fine_repay(customer: Customer):
    total_left_fine = LoanRecord.objects.filter(customer_id=customer.customer_id) \
        .aggregates(total_left_fine=Sum('left_fine'))['total_left_fine']
    if customer.deposit >= total_left_fine:
        customer.deposit -= total_left_fine
        customer.save()
        loan_records = LoanRecord.objects.filter(customer_id=customer.customer_id)
        for loan_record in loan_records:
            if loan_record.left_fine > 0.0:
                _loan_repay(loan_record, loan_record.left_fine)
        return True

    return False


def buy_regular_deposit(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer_id = int(request.POST['customer_id'])
        regular_deposit_id = int(request.POST['regular_deposit_id'])
        purchase_amount = float(request.POST['purchase_amount'])
        purchase_date = datetime.strptime(request.GET['purchase_date'], '%Y-%m-%d')
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')

    try:
        customer = Customer.objects.get(customer_id=customer_id)
        regular_deposit = RegularDeposit.objects.get(regular_deposit_id=regular_deposit_id)
    except Customer.DoesNotExist:
        raise Http404('No such customer')
    except RegularDeposit.DoesNotExist:
        raise Http404('No such regular deposit')

    if not _fine_repay(customer):
        return HttpResponseForbidden('cannot pay fine')
    if customer.deposit < purchase_amount:
        return HttpResponseForbidden('deposit not enough for purchase amount')

    customer.deposit -= purchase_amount
    customer.save()
    RegularDepositInvestment(customer_id=customer_id, regular_deposit_id=regular_deposit_id,
                             purchase_date=purchase_date,
                             due_date=purchase_date + timedelta(days=regular_deposit.return_cycle),
                             purchase_amount=purchase_amount).save()
    response_data = {'msg': 'purchase success'}
    return HttpResponse(json.dumps(response_data))


def buy_fund(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer_id = int(request.POST['customer_id'])
        fund_id = int(request.POST['fund_id'])
        purchase_amount = float(request.POST['purchase_amount'])
        purchase_date = datetime.strptime(request.GET['purchase_date'], '%Y-%m-%d')
        return_cycle = int(request.POST['return_cycle'])
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')

    try:
        customer = Customer.objects.get(customer_id=customer_id)
        Fund.objects.get(fund_id=fund_id)
    except Customer.DoesNotExist:
        raise Http404('No such customer')
    except Fund.DoesNotExist:
        raise Http404('No such fund')

    if not _fine_repay(customer):
        return HttpResponseForbidden('cannot pay fine')
    if customer.deposit < purchase_amount:
        return HttpResponseForbidden('deposit not enough for purchase amount')
    if _get_customer_credit(customer)['credit_level'] > Credit.Credit_Secondary_Account:
        return HttpResponseForbidden('credit level forbidden')

    fund_price = _get_fund_price(fund_id, purchase_date)
    if not fund_price:
        return HttpResponseForbidden('invalid purchase')

    fund_investment = FundInvestment(customer_id=customer_id, fund_id=fund_id,
                                     position_share=purchase_amount / fund_price,
                                     cumulative_purchase_amount=purchase_amount,
                                     purchase_date=purchase_date,
                                     due_date=purchase_date + timedelta(days=return_cycle))

    customer.deposit -= purchase_amount
    customer.save()
    fund_investment.save()
    response_data = {'msg': 'fund purchase success'}
    return HttpResponse(json.dumps(response_data))


def buy_stock(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer_id = int(request.POST['customer_id'])
        stock_id = int(request.POST['stock_id'])
        new_position_share = int(request.POST['new_position_share'])  # 新买入的股数
        purchase_date = datetime.strptime(request.GET['purchase_date'], '%Y-%m-%d')
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')

    try:
        customer = Customer.objects.get(customer_id=customer_id)
        Stock.objects.get(stock_id=stock_id)
    except Customer.DoesNotExist:
        raise Http404('No such customer')
    except Stock.DoesNotExist:
        raise Http404('No such stock')

    if not _fine_repay(customer):
        return HttpResponseForbidden('cannot pay fine')
    stock_price = _get_stock_price(stock_id, purchase_date)
    if not stock_price:
        return HttpResponseForbidden('invalid purchase')
    purchase_amount = stock_price * new_position_share
    if customer.deposit < purchase_amount:
        return HttpResponseForbidden('deposit not enough for purchase amount')
    if _get_customer_credit(customer)['credit_level'] > Credit.Credit_Primary_Account:
        return HttpResponseForbidden('credit level forbidden')

    try:
        stock_investment = StockInvestment.objects.get(customer_id=customer_id, stock_id=stock_id)
        stock_investment.cumulative_purchase_amount += purchase_amount
        stock_investment.position_share += new_position_share
    except StockInvestment.DoesNotExist:
        stock_investment = StockInvestment(customer_id=customer_id, stock_id=stock_id,
                                           position_share=new_position_share,
                                           purchase_date=purchase_date,
                                           cumulative_purchase_amount=purchase_amount)

    customer.deposit -= purchase_amount
    customer.save()
    stock_investment.save()
    response_data = {'msg': 'stock purchase success'}
    return HttpResponse(json.dumps(response_data))

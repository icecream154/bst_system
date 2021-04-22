import json
from datetime import datetime, timedelta

from django.db.models import Sum
from django.http import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseForbidden

from bts.models.constants import DATE_TIME_FORMAT, EM_INVALID_OR_MISSING_PARAMETERS, EM_CANNOT_PAY_FINE, \
    EM_DEPOSIT_NOT_ENOUGH, EM_NO_SUCH_CUSTOMER
from bts.models.customer import Customer
from bts.models.investment import RegularDepositInvestment, FundInvestment, StockInvestment, StockInvestmentRecord
from bts.models.loan import LoanRecord
from bts.models.products import RegularDeposit, Fund, Stock
from bts.services.bank_teller.loan import _loan_repay
from bts.services.market.investment_market import get_fund_price_from_market, get_stock_price_from_market
from bts.services.system.token import fetch_bank_teller_by_token, TOKEN_HEADER_KEY
from bts.utils.request_processor import fetch_parameter_dict


class Credit:
    CREDIT_PRIMARY_ACCOUNT = 1  # 一级账户
    CREDIT_SECONDARY_ACCOUNT = 2  # 二级账户
    CREDIT_THIRD_LEVEL_ACCOUNT = 3  # 三级账户

    CREDIT_PRIMARY_ACCOUNT_LIMIT = 500000.0
    CREDIT_SECONDARY_ACCOUNT_LIMIT = 0


def _get_customer_credit(customer: Customer):
    total_left_payment = customer.loanrecord_set.all() \
        .aggregate(total_left_payment=Sum('left_payment'))['total_left_payment']
    total_left_fine = customer.loanrecord_set.all() \
        .aggregate(total_left_fine=Sum('left_fine'))['total_left_fine']

    credit_info = {
        'deposit': customer.deposit,
        'total_left_payment': total_left_payment,
        'total_left_fine': total_left_fine,
        'net_capital': customer.deposit - total_left_payment - total_left_fine
    }
    if credit_info['net_capital'] > Credit.CREDIT_PRIMARY_ACCOUNT_LIMIT:
        credit_info['credit_level'] = Credit.CREDIT_PRIMARY_ACCOUNT
    elif credit_info['net_capital'] > Credit.CREDIT_SECONDARY_ACCOUNT_LIMIT:
        credit_info['credit_level'] = Credit.CREDIT_SECONDARY_ACCOUNT
    else:
        credit_info['credit_level'] = Credit.CREDIT_THIRD_LEVEL_ACCOUNT

    return credit_info


def get_customer_credit(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer_id = int(request.GET['customer_id'])
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        raise Http404(EM_NO_SUCH_CUSTOMER)

    return HttpResponse(json.dumps(_get_customer_credit(customer)))


def _fine_repay(customer: Customer):
    total_left_fine = customer.loanrecord_set.all() \
        .aggregate(total_left_fine=Sum('left_fine'))['total_left_fine']
    if customer.deposit >= total_left_fine:
        loan_records = customer.loanrecord_set.all()
        for loan_record in loan_records:
            if loan_record.left_fine > 0.0:
                _loan_repay(loan_record, loan_record.left_fine)
        return True

    return False


def buy_regular_deposit(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        parameter_dict = fetch_parameter_dict(request, 'POST')
        customer_id = int(parameter_dict['customer_id'])
        regular_deposit_id = int(parameter_dict['regular_deposit_id'])
        purchase_amount = float(parameter_dict['purchase_amount'])
        purchase_date = datetime.strptime(parameter_dict['purchase_date'], DATE_TIME_FORMAT).date()
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    try:
        customer = Customer.objects.get(customer_id=customer_id)
        regular_deposit = RegularDeposit.objects.get(regular_deposit_id=regular_deposit_id)
    except Customer.DoesNotExist:
        raise Http404(EM_NO_SUCH_CUSTOMER)
    except RegularDeposit.DoesNotExist:
        raise Http404('No such regular deposit')

    if not _fine_repay(customer):
        return HttpResponseForbidden(EM_CANNOT_PAY_FINE)
    if customer.deposit < purchase_amount:
        return HttpResponseForbidden(EM_DEPOSIT_NOT_ENOUGH)

    customer.deposit -= purchase_amount
    customer.save()
    RegularDepositInvestment(customer=customer, regular_deposit=regular_deposit,
                             purchase_date=purchase_date,
                             due_date=purchase_date + timedelta(days=regular_deposit.return_cycle),
                             purchase_amount=purchase_amount, current_deposit=customer.deposit).save()
    response_data = {'msg': 'purchase success'}
    return HttpResponse(json.dumps(response_data))


def buy_fund(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        parameter_dict = fetch_parameter_dict(request, 'POST')
        customer_id = int(parameter_dict['customer_id'])
        fund_id = int(parameter_dict['fund_id'])
        purchase_amount = float(parameter_dict['purchase_amount'])
        purchase_date = datetime.strptime(parameter_dict['purchase_date'], DATE_TIME_FORMAT).date()
        return_cycle = int(parameter_dict['return_cycle'])
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    try:
        customer = Customer.objects.get(customer_id=customer_id)
        fund = Fund.objects.get(fund_id=fund_id)
    except Customer.DoesNotExist:
        raise Http404(EM_NO_SUCH_CUSTOMER)
    except Fund.DoesNotExist:
        raise Http404('No such fund')

    if not _fine_repay(customer):
        return HttpResponseForbidden(EM_CANNOT_PAY_FINE)
    if customer.deposit < purchase_amount:
        return HttpResponseForbidden(EM_DEPOSIT_NOT_ENOUGH)
    if _get_customer_credit(customer)['credit_level'] > Credit.CREDIT_SECONDARY_ACCOUNT:
        return HttpResponseForbidden('credit level forbidden')

    fund_price = get_fund_price_from_market(fund, purchase_date)
    if not fund_price:
        return HttpResponseForbidden('invalid purchase')

    customer.deposit -= purchase_amount
    customer.save()
    fund_investment = FundInvestment(customer=customer, fund=fund,
                                     position_share=purchase_amount / fund_price,
                                     purchase_amount=purchase_amount,
                                     purchase_date=purchase_date,
                                     due_date=purchase_date + timedelta(days=return_cycle),
                                     current_deposit=customer.deposit)
    fund_investment.save()
    response_data = {'msg': 'fund purchase success'}
    return HttpResponse(json.dumps(response_data))


def buy_stock(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        parameter_dict = fetch_parameter_dict(request, 'POST')
        customer_id = int(parameter_dict['customer_id'])
        stock_id = int(parameter_dict['stock_id'])
        new_position_share = int(parameter_dict['new_position_share'])  # 新买入的股数
        purchase_date = datetime.strptime(parameter_dict['purchase_date'], DATE_TIME_FORMAT).date()
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    try:
        customer = Customer.objects.get(customer_id=customer_id)
        stock = Stock.objects.get(stock_id=stock_id)
    except Customer.DoesNotExist:
        raise Http404(EM_NO_SUCH_CUSTOMER)
    except Stock.DoesNotExist:
        raise Http404('No such stock')

    if not _fine_repay(customer):
        return HttpResponseForbidden(EM_CANNOT_PAY_FINE)
    stock_price = get_stock_price_from_market(stock, purchase_date)
    if not stock_price:
        return HttpResponseForbidden('invalid purchase')
    purchase_amount = stock_price * new_position_share
    if customer.deposit < purchase_amount:
        return HttpResponseForbidden(EM_DEPOSIT_NOT_ENOUGH)
    if _get_customer_credit(customer)['credit_level'] > Credit.CREDIT_PRIMARY_ACCOUNT:
        return HttpResponseForbidden('credit level forbidden')

    customer.deposit -= purchase_amount
    try:
        stock_investment = StockInvestment.objects.get(customer=customer, stock=stock)
        stock_investment.cumulative_purchase_amount += purchase_amount
        stock_investment.position_share += new_position_share
        stock_investment.current_deposit = customer.deposit
    except StockInvestment.DoesNotExist:
        stock_investment = StockInvestment(customer=customer, stock=stock,
                                           position_share=new_position_share,
                                           purchase_date=purchase_date,
                                           cumulative_purchase_amount=purchase_amount,
                                           current_deposit=customer.deposit)
    StockInvestmentRecord(customer=customer, stock=stock, position_share=new_position_share,
                          purchase_date=purchase_date, purchase_amount=purchase_amount,
                          current_deposit=customer.deposit).save()
    customer.save()
    stock_investment.save()
    response_data = {'msg': 'stock purchase success'}
    return HttpResponse(json.dumps(response_data))

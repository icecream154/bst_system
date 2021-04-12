import json
from datetime import datetime, timedelta, date

from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseForbidden

from bts.models.customer import Customer
from bts.models.loan import LoanRecord, LoanRepay
from bts.services.system.token import fetch_bank_teller_by_token, TOKEN_HEADER_KEY
from bts.utils.request_processor import fetch_parameter_dict


def _calculate_fine(loan_record: LoanRecord):
    updated = False
    while loan_record.next_overdue_date <= date.today():
        loan_record.left_fine += 0.05 * loan_record.left_payment
        loan_record.next_overdue_date += timedelta(days=loan_record.repay_cycle)
        updated = True

    if updated:
        loan_record.save()


def request_loan(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        parameter_dict = fetch_parameter_dict(request, 'POST')
        customer_id = int(parameter_dict['customer_id'])
        # print(parameter_dict['customer_id'])
        payment = float(parameter_dict['payment'])
        # print(parameter_dict['payment'])
        repay_cycle = int(parameter_dict['repay_cycle'])
        # print(parameter_dict['repay_cycle'])
        created_time = datetime.strptime(parameter_dict['created_time'], '%Y-%m-%d').date()
        # print(parameter_dict['created_time'])
        customer = Customer.objects.get(customer_id=customer_id)
    except (KeyError, ValueError, TypeError, Customer.DoesNotExist):
        return HttpResponseBadRequest('parameter missing or invalid parameter')

    if payment <= 0:
        return HttpResponseBadRequest('invalid parameter')

    try:
        Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        raise Http404('No such customer')

    new_loan_record = LoanRecord(customer=customer, payment=payment,
                                 repay_cycle=repay_cycle,
                                 due_date=created_time + timedelta(days=repay_cycle),
                                 next_overdue_date=created_time + timedelta(days=repay_cycle),
                                 left_payment=payment, left_fine=0.0, created_time=created_time)
    new_loan_record.save()
    response_data = {'msg': 'loan request success', 'loan_record_id': new_loan_record.loan_record_id}
    return HttpResponse(json.dumps(response_data))


def _loan_repay(loan_record: LoanRecord, repay):
    new_loan_repay = LoanRepay(loan_record=loan_record,
                               left_payment_before=loan_record.left_payment,
                               left_fine_before=loan_record.left_fine,
                               repay=repay)
    if repay > loan_record.left_fine + loan_record.left_payment or repay <= 0:
        return False
    if repay > loan_record.left_fine:
        loan_record.left_payment -= repay - loan_record.left_fine
        loan_record.left_fine = 0
    else:
        loan_record.left_fine -= repay
    loan_record.save()
    new_loan_repay.save()  # repay record saved after real load record is modified
    return True


def loan_repay(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        parameter_dict = fetch_parameter_dict(request, 'POST')
        loan_record_id = int(parameter_dict['loan_record_id'])
        repay = float(parameter_dict['repay'])
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')

    if repay <= 0:
        return HttpResponseBadRequest('invalid parameter')

    try:
        loan_record = LoanRecord.objects.get(loan_record_id=loan_record_id)
    except LoanRecord.DoesNotExist:
        raise Http404('No such loan record')

    _calculate_fine(loan_record)
    if _loan_repay(loan_record, repay):
        response_data = {'msg': 'loan repay success'}
        return HttpResponse(json.dumps(response_data))
    return HttpResponseBadRequest('too much repay')


def auto_repay_process(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    load_record_query_set = LoanRecord.objects.all()
    for loan_record in load_record_query_set:
        _calculate_fine(loan_record)
        if loan_record.left_payment > 0 and datetime.now() >= loan_record.due_date:
            customer = Customer.objects.get(customer_id=loan_record.customer)
            curr_repay = 0
            left_payment_before = loan_record.left_payment
            left_fine_before = loan_record.left_fine
            if customer.deposit >= loan_record.left_fine:
                curr_repay += loan_record.left_fine
                customer.deposit -= loan_record.left_fine
                loan_record.left_fine = 0
                if customer.deposit >= loan_record.left_payment:
                    curr_repay += loan_record.left_payment
                    customer.deposit -= loan_record.left_payment
                    loan_record.left_payment = 0

        if curr_repay > 0:
            new_loan_repay = LoanRepay(loan_record=loan_record,
                                       left_payment_before=left_payment_before,
                                       left_fine_before=left_fine_before,
                                       repay=curr_repay)
            loan_record.save()
            customer.save()
            new_loan_repay.save()

    response_data = {'msg': 'auto repay process success'}
    return HttpResponse(json.dumps(response_data))

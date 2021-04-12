import json

from django.http import HttpResponse, HttpResponseBadRequest

from bts.models.customer import Customer
from bts.models.loan import LoanRecord
from bts.services.bank_teller.loan import _calculate_fine
from bts.services.system.token import fetch_bank_teller_by_token, TOKEN_HEADER_KEY


def query_loan_record_by_id(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        loan_record_id = int(request.GET['loan_record_id'])
        loan_record = LoanRecord.objects.get(loan_record_id=loan_record_id)
    except (KeyError, ValueError, TypeError, LoanRecord.DoesNotExist):
        return HttpResponseBadRequest('parameter missing or invalid parameter')
    return HttpResponse(json.dumps(loan_record.to_dict()))


def query_loan_record_by_customer_id(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer_id = int(request.GET['customer_id'])
        customer = Customer.objects.get(customer_id=customer_id)
    except (KeyError, ValueError, TypeError, Customer.DoesNotExist):
        return HttpResponseBadRequest('parameter missing or invalid parameter')

    response_data = []
    for loan_record in customer.loanrecord_set.all():
        _calculate_fine(loan_record)
        response_data.append(loan_record.to_dict())

    return HttpResponse(json.dumps(response_data))

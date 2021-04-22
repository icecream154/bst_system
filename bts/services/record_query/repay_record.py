import json

from django.http import HttpResponse, HttpResponseBadRequest

from bts.models.constants import EM_INVALID_OR_MISSING_PARAMETERS
from bts.models.customer import Customer
from bts.services.system.token import fetch_bank_teller_by_token, TOKEN_HEADER_KEY


def query_repays_by_customer_id(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer_id = int(request.GET['customer_id'])
        customer = Customer.objects.get(customer_id=customer_id)
    except (KeyError, ValueError, TypeError, Customer.DoesNotExist):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    response_data = []
    for loan_record in customer.loanrecord_set.all():
        for loan_repay in loan_record.loanrepay_set.all():
            response_data.append(loan_repay.to_dict())

    return HttpResponse(json.dumps(response_data))

import datetime
import json

from django.http import HttpResponse, Http404, HttpResponseBadRequest

from bts.models.constants import EM_INVALID_OR_MISSING_PARAMETERS, EM_NO_SUCH_CUSTOMER, DATE_TIME_FORMAT
from bts.models.customer import Customer
from bts.models.deposit import DepositRecord
from bts.services.system.token import fetch_bank_teller_by_token, TOKEN_HEADER_KEY
from bts.utils.request_processor import fetch_parameter_dict


def customer_deposit(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        parameter_dict = fetch_parameter_dict(request, 'POST')
        customer_id = int(parameter_dict['customer_id'])
        new_deposit = float(parameter_dict['new_deposit'])
        deposit_date = datetime.strptime(parameter_dict['deposit_date'], DATE_TIME_FORMAT).date()
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    if new_deposit <= 0:
        return HttpResponseBadRequest(EM_INVALID_OR_MISSING_PARAMETERS)

    try:
        customer = Customer.objects.get(customer_id=customer_id)
        customer.deposit += new_deposit
        DepositRecord(customer=customer, payment=new_deposit, current_deposit=customer.deposit,
                      created_time=deposit_date).save()
        customer.save()
        response_data = {'msg': 'customer deposit success'}
        return HttpResponse(json.dumps(response_data))
    except Customer.DoesNotExist:
        raise Http404(EM_NO_SUCH_CUSTOMER)

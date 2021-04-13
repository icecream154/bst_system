import json

from django.http import HttpResponse, HttpResponseBadRequest

from bts.models.customer import Customer
from bts.services.system.token import fetch_bank_teller_by_token, TOKEN_HEADER_KEY


def query_stock_investment_record_by_customer_id(request):
    if not fetch_bank_teller_by_token(request.META[TOKEN_HEADER_KEY]):
        return HttpResponse(content='Unauthorized', status=401)

    try:
        customer_id = int(request.GET['customer_id'])
        customer = Customer.objects.get(customer_id=customer_id)
    except (KeyError, ValueError, TypeError, Customer.DoesNotExist):
        return HttpResponseBadRequest('parameter missing or invalid parameter')

    response_data = []
    for stock_investment_record in customer.stockinvestmentrecord_set.all():
        response_data.append(stock_investment_record.to_dict())

    return HttpResponse(json.dumps(response_data))

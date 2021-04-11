import json

from django.http import HttpResponse, Http404, HttpResponseBadRequest

from bts.models.customer import Customer
from bts.services.system.token import fetch_bank_teller_by_token


def add_customer(request):
    bank_teller = fetch_bank_teller_by_token(request.META['token'])
    if not bank_teller:
        return HttpResponse(content='Unauthorized', status=401)
    # TODO: 未做参数校验

    try:
        name = request.POST['name']
        phone = request.POST['phone']
        id_number = request.POST['id_number']
        deposit = float(request.POST['deposit'])
    except (KeyError, ValueError, TypeError):
        return HttpResponseBadRequest('parameter missing or invalid parameter')

    try:
        Customer.objects.get(id_number=id_number)
        return HttpResponseBadRequest('id number conflict')
    except Customer.DoesNotExist:
        new_customer = Customer(name=name, phone=phone, id_number=id_number,
                                deposit=deposit,
                                bank_teller_id=bank_teller.bank_teller_id)
        new_customer.save()
        response_data = {'msg': 'add new customer success'}
        return HttpResponse(json.dumps(response_data))


def query_customer_by_id_number(request):
    bank_teller = fetch_bank_teller_by_token(request.META['token'])
    if not bank_teller:
        return HttpResponse(content='Unauthorized', status=401)
    try:
        customer = Customer.objects.get(id_number=request.GET['id_number'])
        return HttpResponse(json.dumps(customer.to_dict()))
    except Customer.DoesNotExist:
        raise Http404('No such customer')

import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest

from bts.models.bank_teller import BankTeller
from bts.services.system.token import update_token, fetch_bank_teller_by_token, expire_token, TOKEN_HEADER_KEY


def bank_teller_register(request):
    try:
        account = request.POST['account']
        password = request.POST['password']
        name = request.POST['name']
        phone = request.POST['phone']
    except KeyError:
        return HttpResponseBadRequest("parameter missing or invalid parameter")

    # TODO: 参数校验
    try:
        BankTeller.objects.get(account=account)
        return HttpResponseForbidden("account already exist")
    except BankTeller.DoesNotExist:
        BankTeller(account=account, password=password, name=name, phone=phone).save()
        response_data = {'msg': 'register bank teller success'}
        return HttpResponse(json.dumps(response_data))


def bank_teller_login(request):
    # print('INFO: got request: [%s]' % str(request))
    try:
        bank_teller = BankTeller.objects.get(account=request.POST['account'])
        password = request.POST['password']
    except KeyError:
        return HttpResponseBadRequest("parameter missing or invalid parameter")
    except BankTeller.DoesNotExist:
        # print("INFO: account doesn't exist")
        return HttpResponseForbidden("account doesn't exist")

    if password != bank_teller.password:
        # print("INFO: wrong password: [%s] doesn't match [%s]" % (request.POST['password'], bank_teller.password))
        return HttpResponseForbidden("wrong password")

    new_token, new_expire_time = update_token(bank_teller)
    response_data = {'token': new_token, 'expire_time:': new_expire_time}
    # print('INFO: build response data [%s] success' % str(response_data))
    return HttpResponse(json.dumps(response_data))


def bank_teller_logout(request):
    token = request.META.get(TOKEN_HEADER_KEY)
    bank_teller = fetch_bank_teller_by_token(token)
    if bank_teller:
        expire_token(token)
        response_data = {'msg': 'logout success'}
        return HttpResponse(json.dumps(response_data))
    else:
        print(bank_teller)
        return HttpResponseForbidden("invalid token")
import json

from django.http import HttpRequest


def fetch_parameter_dict(request: HttpRequest, request_type: str):
    if request_type == 'GET':
        return request.GET
    parameter_dict = {}
    if request_type == 'POST':
        parameter_dict = request.POST
    if 'application/json' in request.META['CONTENT_TYPE']:
        parameter_dict = json.loads(request.body.decode('utf8'))
    return parameter_dict

import requests
import json
from django.test import Client

BST_BASE_URL = 'http://localhost:8000/bts'
TOKEN_HEADER_KEY = 'AUTHORIZATION'


def do_request(request_type: str, url: str, params: dict = None, headers: dict = None, data: dict = None):
    response = requests.request(request_type, BST_BASE_URL + url, params=params, headers=headers, data=data)
    response_dict = None
    if response.status_code == 200:
        try:
            response_dict = json.loads(response.text)
        except json.decoder.JSONDecodeError as ex:
            print(ex)
    elif response.status_code != 404:
        response_dict = response.text
    return response.status_code, response_dict

    # client = Client()
    # if headers is None:
    #     headers = {}
    # if request_type == "POST":
    #     response = client.post(BST_BASE_URL + url,
    #                            data=data, **headers)
    # else:
    #     response = client.get(BST_BASE_URL + url,
    #                           data=params, **headers)
    # response_dict = response.content.decode('utf-8')
    # if response.status_code == 200:
    #     response_dict = json.loads(response_dict)
    # return response.status_code, response_dict


def do_get_request(url: str, params: dict = None, headers: dict = None, data: dict = None):
    return do_request('GET', url, params, headers, data)


def do_post_request(url: str, params: dict = None, headers: dict = None, data: dict = None):
    return do_request('POST', url, params, headers, data)

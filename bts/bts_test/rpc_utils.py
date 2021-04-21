import requests
import json

BST_BASE_URL = 'http://localhost:8000/bts'


def do_request(request_type: str, url: str, params: dict = None, headers: dict = None, data: dict = None):
    response = requests.request(request_type, BST_BASE_URL + url, params=params, headers=headers, data=data)
    # print(response.request.headers)
    response_dict = None
    if response.status_code == 200:
        try:
            response_dict = json.loads(response.text)
        except json.decoder.JSONDecodeError as ex:
            print(ex)
    elif response.status_code != 404:
        response_dict = response.text
    return response.status_code, response_dict


def do_get_request(url: str, params: dict = None, headers: dict = None, data: dict = None):
    return do_request('GET', url, params, headers, data)


def do_post_request(url: str, params: dict = None, headers: dict = None, data: dict = None):
    return do_request('POST', url, params, headers, data)
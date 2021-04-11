import requests
import json

BST_BASE_URL = 'http://10.176.122.173:8012'


def do_request(request_type: str, url: str, params: dict = None, headers: dict = None, data: dict = None):
    response = requests.request(request_type, BST_BASE_URL + url, params=params, headers=headers, data=data)
    response_dict = None
    try:
        response_dict = json.loads(response.text)
    except json.decoder.JSONDecodeError as ex:
        print(ex)
    return response.status_code, response_dict

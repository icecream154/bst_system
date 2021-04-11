import requests
import json

BST_BASE_URL = 'http://localhost:8000'


def do_request(request_type: str, url: str, params: dict = None, headers: dict = None, data: dict = None):
    response = requests.request(request_type, BST_BASE_URL + url, params=params, headers=headers, data=data)
    response_dict = None
    try:
        response_dict = json.loads(response.text)
    except json.decoder.JSONDecodeError as ex:
        print(ex)
    return response.status_code, response_dict


def do_get_request(url: str, params: dict = None, headers: dict = None, data: dict = None):
    response = requests.get(BST_BASE_URL + url, params=params, headers=headers, data=data)
    response_dict = None
    try:
        response_dict = json.loads(response.text)
    except json.decoder.JSONDecodeError as ex:
        print(ex)
    return response.status_code, response_dict


def do_post_request(url: str, params: dict = None, headers: dict = None, data: dict = None):
    response = requests.post(BST_BASE_URL + url, params=params, headers=headers, data=data)
    response_dict = None
    try:
        response_dict = json.loads(response.text)
    except json.decoder.JSONDecodeError as ex:
        print(ex)
    return response.status_code, response_dict


def sys_login(username: str, password: str):
    params_dict = {'username': username, 'password': password}
    return do_post_request('/system/login', data=params_dict)


def sys_logout(token: str):
    return do_get_request('/system/logout', headers={'token': token})


if __name__ == '__main__':
    status_code, response_dict = sys_login('BST1', 'imbus123');
    print(status_code)
    print(response_dict)

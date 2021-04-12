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


def sys_register(account: str, password: str, name: str, phone: str):
    return do_post_request('/system/register', data={'account': account, 'password': password,
                                                     'name': name, 'phone': phone})


def sys_login(username: str, password: str):
    params_dict = {'account': username, 'password': password}
    return do_post_request('/system/login', data=params_dict)


def sys_logout(token: str):
    return do_post_request('/system/logout', headers={'token': token})


def add_customer(token: str, name: str, phone: str, id_number: str, deposit: float):
    return do_post_request('/customer/add', headers={'token': token},
                           data={'name': name, 'phone': phone, 'id_number': id_number, 'deposit': deposit})


def query_customer_by_id_number(token: str, id_number: str):
    return do_get_request('/customer/query_by_id_number', headers={'token': token},
                          params={'id_number': id_number})


def customer_deposit(token: str, customer_id: int, new_deposit: float):
    return do_post_request('/deposit', headers={'token': token}, data={'customer_id': customer_id,
                                                                       'new_deposit': new_deposit})


def customer_loan(token: str, customer_id: int, payment: float, repay_cycle: int, created_time: str):
    return do_post_request('/loan/request_loan', headers={'token': token}, data={'customer_id': customer_id,
                                                                                 'payment': payment,
                                                                                 'repay_cycle': repay_cycle,
                                                                                 'created_time': created_time})


def loan_query_record_by_id(token: str, loan_record_id: int):
    return do_get_request('/loan/query_by_record_id',  headers={'token': token},
                          params={'loan_record_id': loan_record_id})


def loan_query_record_by_customer_id(token: str, customer_id: int):
    return do_get_request('/loan/query_by_customer_id', headers={'token': token}, params={'customer_id': customer_id})


def customer_loan_repay(token: str, loan_record_id: int, repay: float):
    return do_post_request('/loan/repay', headers={'token': token}, data={'loan_record_id': loan_record_id,
                                                                          'repay': repay})


def loan_auto_repay():
    pass


def show_info(status_code: int, response_dict: dict):
    print('status_code[%d] and response: [%s]' % (status_code, response_dict))


if __name__ == '__main__':
    # 注册两个柜员
    status_code, response_dict = sys_register('BTS1', 'imbus123', '柜员一', '13966667777')
    show_info(status_code, response_dict)
    status_code, response_dict = sys_register('BTS2', 'imbus123', '柜员二', '13966667777')
    show_info(status_code, response_dict)

    # 柜员一登录
    status_code, response_dict = sys_login('BTS1', 'imbus123')
    show_info(status_code, response_dict)

    # 柜员一添加新客户
    bt_token = response_dict['token']
    status_code, response_dict = add_customer(bt_token, name='客户一', phone='13100001234',
                                              id_number='330888855550001', deposit=1000.0)
    show_info(status_code, response_dict)
    # 查询该新添加的客户
    status_code, response_dict = query_customer_by_id_number(bt_token, '330888855550001')
    show_info(status_code, response_dict)

    # 给该客户存款200
    test_customer_id = response_dict['customer_id']
    status_code, response_dict = customer_deposit(bt_token, test_customer_id, 200.0)
    show_info(status_code, response_dict)
    # 重新查询，存款变为1200
    status_code, response_dict = query_customer_by_id_number(bt_token, '330888855550001')
    show_info(status_code, response_dict)

    # 客户贷款300
    status_code, response_dict = customer_loan(token=bt_token, customer_id=test_customer_id, payment=300,
                                               repay_cycle=7, created_time='2021-4-1')
    show_info(status_code, response_dict)
    new_loan_record_id = response_dict['loan_record_id']
    # 查询到这笔贷款
    status_code, response_dict = loan_query_record_by_customer_id(bt_token, test_customer_id)
    show_info(status_code, response_dict)

    # 还款215，由于已经超期，应该有15元用于支付罚款
    status_code, response_dict = customer_loan_repay(bt_token, loan_record_id=new_loan_record_id, repay=215)
    show_info(status_code, response_dict)

    # 再次查询，剩余未还金额应为100
    status_code, response_dict = loan_query_record_by_id(bt_token, new_loan_record_id)
    show_info(status_code, response_dict)

    # 柜员登出
    status_code, response_dict = sys_logout(bt_token)
    show_info(status_code, response_dict)

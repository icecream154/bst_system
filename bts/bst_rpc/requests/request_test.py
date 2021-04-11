from bts.bst_rpc.requests.customer_request import get_customers, add_customers
from bts.bst_rpc.requests.sys_request import sys_login

if __name__ == '__main__':
    """
    管理员账号：
    BA2103158036
    imbus123

    柜员一：
    JT2104092090
    imbus123
    """

    _, sys_login_response_dict = sys_login(username='JT2104092090', password='imbus123')
    counter_token = sys_login_response_dict['token']

    status_code, get_customers_response_dict = get_customers(1, 10, token=counter_token)
    print(get_customers_response_dict['list'])

    status_code, add_customers_response_dict = \
        add_customers(name='客户二', sex=2, idtype=1, id_number='330123412340002', phone='13100000002',
                      email='kh2@bst.com', address='上海市虹口区松花江路2500号', permanent_address='上海市虹口区松花江路2500号',
                      alternate_name='联系人二', alternate_phone='13100001002', transaction_code='6101',
                      branch_num='fdse001', token=counter_token)
    print('add response got code %d and response %s' % (status_code, add_customers_response_dict))

    status_code, get_customers_response_dict = get_customers(1, 10, token=counter_token)
    print(get_customers_response_dict['list'])

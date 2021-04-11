from bts.bst_rpc.requests.do_request import do_request


def get_customers(page_num: int, page_size: int, params: dict = None, token: str = None):
    params_dict = {}
    if page_num:
        params_dict['pageNum'] = page_num
    if page_size:
        params_dict['pageSize'] = page_size
    if not params:
        params = {'orderBy': 'order by updateTime desc'}
    params_dict['params'] = str(params)
    return do_request('GET', '/customer', params=params_dict, headers={'login-token': token})

"""
address: "上海市虹口区松花江路2500号"
alternateName: "联系人一"
alternatePhone: "13100001001"
branchNum: "fdse001"
email: "kh1@bst.com"
idnumber: "330123412340001"
idtype: 1
name: "客户一"
permanentAddress: "上海市虹口区松花江路2500号"
phone: "13100000001"
sex: 1
transactionCode: "6101"
"""


def add_customers(name: str, sex: int, idtype: int, id_number: str, phone: str, email: str, address: str,
                  permanent_address: str, alternate_name: str, alternate_phone: str, transaction_code: str,
                  branch_num: str, token: str = None):
    data_dict = {
        'idnumber': id_number,
            'address': address,
            'alternateName': alternate_name,
            'alternatePhone': alternate_phone,
            'branchNum': branch_num,
            'email': email,
            'idtype': idtype,
            'name': name,
            'permanentAddress': permanent_address,
            'phone': phone,
            'sex': sex,
            'transactionCode': transaction_code
    }
    return do_request('POST', '/customer',
                      headers={'login-token': token, 'Content-Type': 'application/json;charset=UTF-8'},
                      data=data_dict)

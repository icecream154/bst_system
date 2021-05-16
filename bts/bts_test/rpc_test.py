from bts.bts_test.rpc_utils import do_get_request, do_post_request, TOKEN_HEADER_KEY


def sys_register(account: str, password: str, name: str, phone: str = None):
    if phone is not None:
        return do_post_request('/system/register',
                               data={'account': account, 'password': password, 'name': name, 'phone': phone})
    else:
        return do_post_request('/system/register', data={'account': account, 'password': password, 'name': name})


def sys_login(username: str, password: str = None):
    if password is not None:
        params_dict = {'account': username, 'password': password}
    else:
        params_dict = {'account': username}
    return do_post_request('/system/login', data=params_dict)


def sys_logout(token: str):
    return do_post_request('/system/logout', headers={TOKEN_HEADER_KEY: token})


# 添加客户
def add_customer(token: str, name: str, phone: str, id_number: str, deposit: float = None):
    if deposit is not None:
        return do_post_request('/customer/add', headers={TOKEN_HEADER_KEY: token},
                               data={'name': name, 'phone': phone, 'id_number': id_number, 'deposit': deposit})
    else:
        return do_post_request('/customer/add', headers={TOKEN_HEADER_KEY: token},
                               data={'name': name, 'phone': phone, 'id_number': id_number})


# 通过身份证查询客户
def query_customer_by_id_number(token: str, id_number: str = None):
    if id_number is not None:
        return do_get_request('/customer/query_by_id_number', headers={TOKEN_HEADER_KEY: token},
                              params={'id_number': id_number})
    else:
        return do_get_request('/customer/query_by_id_number', headers={TOKEN_HEADER_KEY: token})


# 客户存款
def customer_deposit(token: str, customer_id: int, deposit_date: str, new_deposit: float = None):
    if new_deposit is not None:
        return do_post_request('/deposit', headers={TOKEN_HEADER_KEY: token}, data={'customer_id': customer_id,
                                                                                    'new_deposit': new_deposit,
                                                                                    'deposit_date': deposit_date})
    else:
        return do_post_request('/deposit', headers={TOKEN_HEADER_KEY: token}, data={'customer_id': customer_id})


# 客户贷款
def customer_loan(token: str, customer_id: int, payment: float, repay_cycle: int, created_time: str = None):
    if created_time is not None:
        return do_post_request('/loan/request_loan', headers={TOKEN_HEADER_KEY: token},
                               data={'customer_id': customer_id,
                                     'payment': payment,
                                     'repay_cycle': repay_cycle,
                                     'created_time': created_time})
    else:
        return do_post_request('/loan/request_loan', headers={TOKEN_HEADER_KEY: token},
                               data={'customer_id': customer_id,
                                     'payment': payment,
                                     'repay_cycle': repay_cycle})


# 查询指定ID的贷款记录
def loan_query_record_by_id(token: str, loan_record_id: int):
    return do_get_request('/loan/query_by_record_id', headers={TOKEN_HEADER_KEY: token},
                          params={'loan_record_id': loan_record_id})


# 查询客户的所有贷款
def loan_query_record_by_customer_id(token: str, customer_id: int):
    return do_get_request('/loan/query_by_customer_id', headers={TOKEN_HEADER_KEY: token},
                          params={'customer_id': customer_id})


# 客户进行贷款还款
def customer_loan_repay(token: str, loan_record_id: int, repay: float = None):
    if repay is not None:
        return do_post_request('/loan/repay', headers={TOKEN_HEADER_KEY: token}, data={'loan_record_id': loan_record_id,
                                                                                       'repay': repay})
    else:
        return do_post_request('/loan/repay', headers={TOKEN_HEADER_KEY: token},
                               data={'loan_record_id': loan_record_id})


# 发起日终处理
def loan_auto_repay(token: str):
    return do_post_request('/loan/auto_repay', headers={TOKEN_HEADER_KEY: token})


# 发行定期理财产品
def issue_regular_deposit(token: str, regular_deposit_name: str,
                          issue_date: str, return_cycle: int, return_rate: float = None):
    if return_rate is not None:
        return do_post_request('/market/issue_regular_deposit', headers={TOKEN_HEADER_KEY: token},
                               data={'regular_deposit_name': regular_deposit_name, 'issue_date': issue_date,
                                     'return_cycle': return_cycle, 'return_rate': return_rate})
    else:
        return do_post_request('/market/issue_regular_deposit', headers={TOKEN_HEADER_KEY: token},
                               data={'regular_deposit_name': regular_deposit_name, 'issue_date': issue_date,
                                     'return_cycle': return_cycle})


# 发行基金
def issue_fund(token: str, fund_name: str, issue_date: str, issue_price: float = None):
    if issue_price is not None:
        return do_post_request('/market/issue_fund', headers={TOKEN_HEADER_KEY: token},
                               data={'fund_name': fund_name, 'issue_date': issue_date,
                                     'issue_price': issue_price})
    else:
        return do_post_request('/market/issue_fund', headers={TOKEN_HEADER_KEY: token},
                               data={'fund_name': fund_name, 'issue_date': issue_date})


# 发行股票
def issue_stock(token: str, stock_name: str, issue_date: str, issue_price: float = None):
    if issue_price is not None:
        return do_post_request('/market/issue_stock', headers={TOKEN_HEADER_KEY: token},
                               data={'stock_name': stock_name, 'issue_date': issue_date,
                                     'issue_price': issue_price})
    else:
        return do_post_request('/market/issue_stock', headers={TOKEN_HEADER_KEY: token},
                               data={'stock_name': stock_name, 'issue_date': issue_date})


# 获取基金价格
def get_fund_price(fund_id: int, search_date: str = None):
    if search_date is not None:
        return do_get_request('/market/get_fund_price', params={'fund_id': fund_id, 'search_date': search_date})
    else:
        return do_get_request('/market/get_fund_price', params={'fund_id': fund_id})


# 获取股票价格
def get_stock_price(fund_id: int, search_date: str = None):
    if search_date is not None:
        return do_get_request('/market/get_stock_price', params={'stock_id': fund_id, 'search_date': search_date})
    else:
        return do_get_request('/market/get_stock_price', params={'stock_id': fund_id})


# 查询基金
def query_funds(product_id: int = None):
    if product_id is not None:
        return do_get_request('/market/query_funds', params={'product_id': product_id})
    else:
        return do_get_request('/market/query_funds')


# 查询股票
def query_stocks(product_id: int = None):
    if product_id is not None:
        return do_get_request('/market/query_stocks', params={'product_id': product_id})
    else:
        return do_get_request('/market/query_stocks')


# 查询定期理财
def query_regular_deposits(product_id: int = None):
    if product_id is not None:
        return do_get_request('/market/query_regular_deposits', params={'product_id': product_id})
    else:
        return do_get_request('/market/query_regular_deposits')


# 购买定期理财产品
def buy_regular_deposit(token: str, customer_id: int, regular_deposit_id: int,
                        purchase_amount: float, purchase_date: str = None):
    if purchase_date is not None:
        return do_post_request('/investment/buy_regular_deposit', headers={TOKEN_HEADER_KEY: token},
                               data={'customer_id': customer_id, 'regular_deposit_id': regular_deposit_id,
                                     'purchase_amount': purchase_amount, 'purchase_date': purchase_date})
    else:
        return do_post_request('/investment/buy_regular_deposit', headers={TOKEN_HEADER_KEY: token},
                               data={'customer_id': customer_id, 'regular_deposit_id': regular_deposit_id,
                                     'purchase_amount': purchase_amount})


# 购买基金产品
def buy_fund(token: str, customer_id: int, fund_id: int,
             purchase_amount: float, purchase_date: str, return_cycle: int = None):
    if return_cycle is not None:
        return do_post_request('/investment/buy_fund', headers={TOKEN_HEADER_KEY: token},
                               data={'customer_id': customer_id, 'fund_id': fund_id,
                                     'purchase_amount': purchase_amount, 'purchase_date': purchase_date,
                                     'return_cycle': return_cycle})
    else:
        return do_post_request('/investment/buy_fund', headers={TOKEN_HEADER_KEY: token},
                               data={'customer_id': customer_id, 'fund_id': fund_id,
                                     'purchase_amount': purchase_amount, 'purchase_date': purchase_date})


# 购买股票产品
def buy_stock(token: str, customer_id: int, stock_id: int,
              new_position_share: float, purchase_date: str = None):
    if purchase_date is not None:
        return do_post_request('/investment/buy_stock', headers={TOKEN_HEADER_KEY: token},
                               data={'customer_id': customer_id, 'stock_id': stock_id,
                                     'new_position_share': new_position_share, 'purchase_date': purchase_date})
    else:
        return do_post_request('/investment/buy_stock', headers={TOKEN_HEADER_KEY: token},
                               data={'customer_id': customer_id, 'stock_id': stock_id,
                                     'new_position_share': new_position_share})


# 查询用户信用等级
def get_customer_credit(token: str, customer_id: int = None):
    if customer_id is not None:
        return do_get_request("/investment/get_customer_credit", headers={TOKEN_HEADER_KEY: token},
                              params={"customer_id": customer_id})
    else:
        return do_get_request("/investment/get_customer_credit", headers={TOKEN_HEADER_KEY: token})


# 查询用户基金投资情况
def query_customer_fund_invest(token: str, customer_id: int, query_date: str = None):
    if query_date is not None:
        return do_get_request("/investment/query_customer_fund_invest", headers={TOKEN_HEADER_KEY: token},
                              params={"customer_id": customer_id, "query_date": query_date})
    else:
        return do_get_request("/investment/query_customer_fund_invest", headers={TOKEN_HEADER_KEY: token},
                              params={"customer_id": customer_id})


# 查询用户股票投资情况
def query_customer_stock_invest(token: str, customer_id: int, query_date: str = None):
    if query_date is not None:
        return do_get_request("/investment/query_customer_stock_invest", headers={TOKEN_HEADER_KEY: token},
                              params={"customer_id": customer_id, "query_date": query_date})
    else:
        return do_get_request("/investment/query_customer_stock_invest", headers={TOKEN_HEADER_KEY: token},
                              params={"customer_id": customer_id})


# 查询用户定期理财投资情况
def query_customer_regular_deposit_invest(token: str, customer_id: int = None):
    if customer_id is not None:
        return do_get_request("/investment/query_customer_regular_deposit_invest", headers={TOKEN_HEADER_KEY: token},
                              params={"customer_id": customer_id})
    else:
        return do_get_request("/investment/query_customer_regular_deposit_invest", headers={TOKEN_HEADER_KEY: token})


# 查询用户存款记录
def query_deposits_by_customer_id(token: str, customer_id: int = None):
    if customer_id is not None:
        return do_get_request("/record_query/deposit", headers={TOKEN_HEADER_KEY: token},
                              params={"customer_id": customer_id})
    else:
        return do_get_request("/record_query/deposit", headers={TOKEN_HEADER_KEY: token})


# 查询用户还款记录
def query_repays_by_customer_id(token: str, customer_id: int = None):
    if customer_id is not None:
        return do_get_request("/record_query/repay", headers={TOKEN_HEADER_KEY: token},
                              params={"customer_id": customer_id})
    else:
        return do_get_request("/record_query/repay", headers={TOKEN_HEADER_KEY: token})


# 查询用户股票投资记录
def query_stock_investment_by_customer_id(token: str, customer_id: int = None):
    if customer_id is not None:
        return do_get_request("/record_query/stock_investment", headers={TOKEN_HEADER_KEY: token},
                              params={"customer_id": customer_id})
    else:
        return do_get_request("/record_query/stock_investment", headers={TOKEN_HEADER_KEY: token})


def show_info(param_status_code: int, param_response_dict: dict):
    print('status_code[%d] and response: [%s]' % (param_status_code, param_response_dict))


# 数据库初始化脚本
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
    new_customer_id = response_dict['customer_id']
    status_code, response_dict = customer_deposit(bt_token, new_customer_id, 200.0, '2021-3-27')
    show_info(status_code, response_dict)
    # 重新查询，存款变为1200
    status_code, response_dict = query_customer_by_id_number(bt_token, '330888855550001')
    show_info(status_code, response_dict)

    # 客户贷款300
    status_code, response_dict = customer_loan(token=bt_token, customer_id=new_customer_id, payment=300,
                                               repay_cycle=7, created_time='2021-4-1')
    show_info(status_code, response_dict)
    new_loan_record_id = response_dict['loan_record_id']
    # 查询到这笔贷款
    status_code, response_dict = loan_query_record_by_customer_id(bt_token, new_customer_id)
    show_info(status_code, response_dict)

    # 还款215，由于已经超期，应该有15元用于支付罚款
    status_code, response_dict = customer_loan_repay(bt_token, loan_record_id=new_loan_record_id, repay=215)
    show_info(status_code, response_dict)

    # 再次查询，剩余未还金额应为100
    status_code, response_dict = loan_query_record_by_id(bt_token, new_loan_record_id)
    show_info(status_code, response_dict)

    # 发行定期理财产品
    status_code, response_dict = issue_regular_deposit(bt_token, '定期理财一号', '2021-3-9', 9, 0.07)
    show_info(status_code, response_dict)
    new_regular_deposit_id = response_dict['regular_deposit_id']

    # 发行基金
    status_code, response_dict = issue_fund(bt_token, '基金一号', '2021-3-20', 3.2)
    show_info(status_code, response_dict)
    new_fund_id = response_dict['fund_id']

    # 发行股票
    status_code, response_dict = issue_stock(bt_token, '浦发银行', '2021-3-30', 15)
    show_info(status_code, response_dict)
    new_stock_id = response_dict['stock_id']

    # 购买定期理财产品，买太多，失败
    status_code, response_dict = buy_regular_deposit(bt_token, new_customer_id,
                                                     new_regular_deposit_id, 20000, '2021-4-9')
    show_info(status_code, response_dict)

    # 再次购买定期理财产品
    status_code, response_dict = buy_regular_deposit(bt_token, new_customer_id,
                                                     new_regular_deposit_id, 200, '2021-4-9')
    show_info(status_code, response_dict)

    # 购买股票,失败，因为不是一级账户
    status_code, response_dict = buy_stock(bt_token, new_customer_id, new_stock_id, 20, '2021-4-21')
    show_info(status_code, response_dict)

    # 存入500000，摇身一变变为一级账户
    status_code, response_dict = customer_deposit(bt_token, new_customer_id, 500000, '2021-4-22')
    show_info(status_code, response_dict)

    # 再次购买股票
    status_code, response_dict = buy_stock(bt_token, new_customer_id, new_stock_id, 20, '2021-4-23')
    show_info(status_code, response_dict)

    # 重新查询，存款变为500700, 定期200加股票300共用去500
    status_code, response_dict = query_customer_by_id_number(bt_token, '330888855550001')
    show_info(status_code, response_dict)

    # 柜员登出
    status_code, response_dict = sys_logout(bt_token)
    show_info(status_code, response_dict)

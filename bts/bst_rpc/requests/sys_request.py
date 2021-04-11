from bts.bst_rpc.requests.do_request import do_request


def sys_login(username: str, password: str):
    params_dict = {'username': username, 'password': password}
    return do_request('POST', '/system/login/restful', params_dict)


def sys_logout(token: str):
    return do_request('GET', '/system/logout', headers={'login-token': token})

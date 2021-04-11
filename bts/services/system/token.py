import time

from bts.models.bank_teller import BankTeller

# dictionary to store tokens and BankTellers ({str: (BankTeller, float)})
token_dict = {}
# default expire time set to 10800 seconds (3 hour)
_EXPIRE_TIME = 10800


def _get_token_by_id(token_dictionary: {str: (BankTeller, float)}, bank_teller_id: int):
    return [k for k, v in token_dictionary.items() if v[0].bank_teller_id == bank_teller_id]


def _generate_token_string(bank_teller: BankTeller):
    return "fake token " + str(bank_teller)


def update_token(bank_teller: BankTeller):
    token_by_id = _get_token_by_id(token_dict, bank_teller.bank_teller_id)
    if len(token_by_id) == 1:
        del token_dict[token_by_id[0]]

    new_token = _generate_token_string(bank_teller)
    new_expire_time = time.time() + _EXPIRE_TIME
    token_dict[new_token] = (bank_teller, new_expire_time)
    return new_token, new_expire_time


def fetch_bank_teller_by_token(token: str):
    try:
        bank_teller, expire_time = token_dict[token]
        if time.time() > expire_time:
            del token_dict[token]
            return None
        return bank_teller
    except KeyError:
        return None


def expire_token(token: str):
    if token in token_dict:
        del token_dict[token]

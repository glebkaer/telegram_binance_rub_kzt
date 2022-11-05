import requests


def get_pretty_results(data: dict) -> list[dict]:
    """
    :param data: dict of ansert from binance
    :return: List of dicts with results
    """
    res_val = []
    for idx, val in enumerate(data['data']):
        res_val.append(
            {
                'rate': val['adv']['price'],
                'min_amount': val['adv']['minSingleTransAmount'],
                'max_amount': val['adv']['maxSingleTransAmount'],
                'monthOrderCount': val['advertiser']['monthOrderCount'],
                'monthFinishRate': val['advertiser']['monthFinishRate'] * 100,
                'USDTavailable': val['adv']['tradableQuantity']
            })
    return res_val


def get_rate(fiat_cur: str = 'RUB', asset_cur: str = 'USDT',
             tradetype: str = 'BUY', paytypes: str = 'TinkoffNew',
             page: int = 1) -> dict:
    """
    :param fiat_cur: USDT
    :param asset_cur: RUB or KZT
    :param tradetype: BUY or SELL
    :param paytypes: TinkoffNew or KaspiBank
    :param page: Number of page to be scanned
    :return: DICT answer from binance
    """
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
    params = {
        'page': page,
        'rows': 20,
        'asset': asset_cur,
        "fiat": fiat_cur,
        "tradeType": tradetype,
        'proMerchantAds': False,
        "payTypes": [paytypes]
    }
    return get_pretty_results(requests.post(url, json=params).json())


def get_simple_output_values_for_bot() -> str:
    """
    :return:
    """
    rub_dict = get_rate('RUB', 'USDT', 'BUY', 'TinkoffNew')
    kzt_dict = get_rate('KZT', 'USDT', 'SELL', 'KaspiBank')
    for rub_val, kzt_val in zip(rub_dict, kzt_dict):
        return_str = f"""
Actual rate RUB to KZT - {(float(kzt_val['rate'])/float(rub_val['rate'])):.2f}
Rate RUB to USDT - {rub_val['rate']}
Min sum in RUB - {rub_val['min_amount']}
Rate USDT to KZT - {kzt_val['rate']}
        """
        return return_str


def get_best_cur(listofcurs: list[dict], sumtochange: int, checkifbuy: bool = 1) -> dict:
    for cur_dict in listofcurs:
        for cur_val in cur_dict:
            if float(cur_val['min_amount']) <= sumtochange if checkifbuy else sumtochange*float(cur_val['rate']) <= float(cur_val['max_amount']):
                return cur_val
    return None


def get_complex_output_values_for_bot(sumtochange: int = 10000) -> str:
    """
    :return:
    """
    rub_list, kzt_list = [], []
    for i in range(1, 11):
        rub_list.append(get_rate('RUB', 'USDT', 'BUY', 'TinkoffNew', i))
        kzt_list.append(get_rate('KZT', 'USDT', 'SELL', 'KaspiBank', i))
    rub_best_cur_dict = get_best_cur(rub_list, sumtochange)
    if rub_best_cur_dict is not None:
        kzt_best_cur_dict = get_best_cur(kzt_list, sumtochange/float(rub_best_cur_dict['rate']), 0)
        if kzt_best_cur_dict is not None:
            return f"""
Actual rate RUB to KZT - {(float(kzt_best_cur_dict['rate'])/float(rub_best_cur_dict['rate'])):.2f}
Rate RUB to USDT - {rub_best_cur_dict['rate']}
Rate USDT to KZT - {kzt_best_cur_dict['rate']}
Seller account RUB to USDT (Count of orders/Finish rate) - {rub_best_cur_dict['monthOrderCount']}/{rub_best_cur_dict['monthFinishRate']:.2f}
Seller account USDT to KZT (Count of orders/Finish rate) - {kzt_best_cur_dict['monthOrderCount']}/{kzt_best_cur_dict['monthFinishRate']:.2f}
Amount in KZT - {sumtochange*float(kzt_best_cur_dict['rate'])/float(rub_best_cur_dict['rate'])}
                """
        else:
            return f"""
            No available ways today
        """
    else:
        return f"""
No available ways today
"""
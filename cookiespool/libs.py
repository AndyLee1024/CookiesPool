import requests
from cookiespool.config import PROXY_POOL_URL


def get_random_proxy():
    """
    :return: proxy
    """
    proxy = requests.get(PROXY_POOL_URL).text.strip()
    print('http://{}'.format(proxy))
    return proxy


def proxy_wrapper_for_requests():
    proxy = get_random_proxy()
    return {
        "http": proxy,
        "https": proxy
    }

import requests


def dict_to_str(ddd):
    line = ''
    for k, v in ddd.items():
        line += f'{k}={v}; '
    return line


url = 'http://172.19.245.95:5022/xiaohongshu/random'
cookies = requests.get(url).json()

cookie_str = dict_to_str(cookies)
print(cookie_str)

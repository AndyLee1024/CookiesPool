import time

import requests

from cookiespool.config import TEST_URL_MAP
from cookiespool.libs import get_user_agent


def get_zhihu_cookie(username, password):
    result = {
        'status': 3
    }
    try:
        headers = {
            "referer": "https://www.zhihu.com/search?type=content&q=python&utm_content=search_preset",
            "user-agent": get_user_agent(),
        }
        res = requests.post(TEST_URL_MAP.get('zhihu'), headers=headers)
        if res.status_code == 200:
            result['status'] = 1
            result['content'] = f'"{res.text}|{int(time.time())}";'
    except Exception as e:
        print('got exception -> {}'.format(e), flush=True)
    finally:
        print('Successful to get cookies', result)
        return result


if __name__ == '__main__':
    get_zhihu_cookie(username='test', password='test')

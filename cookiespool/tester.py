import json
import requests
from requests.exceptions import ConnectionError
from cookiespool.db import *
from cookiespool.libs import proxy_wrapper_for_requests, get_user_agent
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from retrying import retry

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

# Get list of user agents.
user_agents = user_agent_rotator.get_user_agents()


# Get Random User Agent String.
@retry(stop_max_attempt_number=5)
def send_request(url, headers, cookies):
    proxy = proxy_wrapper_for_requests()
    res = requests.get(url, headers, proxies=proxy, cookies=cookies, timeout=5)
    print('starting test request ..')
    if res.ok:
        if res.text.find('datePublished') > -1:
            return 'cool'
        else:
            raise KeyError('cookies has been outdated')
    else:
        raise ConnectionRefusedError('something went wrong')


class ValidTester(object):
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        cookies_groups = self.cookies_db.all()
        if len(cookies_groups) == 0:
            print('没有Cookies 无法进行测试', flush=True)
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


class WeiboValidTester(ValidTester):
    def __init__(self, website='weibo'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print('正在测试Cookies', '用户名', username, flush=True)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法', username, flush=True)
            self.cookies_db.delete(username)
            print('删除Cookies', username, flush=True)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            headers = {
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'Referer': 'https://www.xiaohongshu.com/',
                'User-Agent': get_user_agent(1)
            }
            res = send_request(test_url, cookies=cookies, headers=headers)
            if res == 'cool':
                print('Cookies有效', username, flush=True)
            else:
                print(response.status_code, response.headers)
                print('Cookies失效', username, flush=True)
                self.cookies_db.delete(username)
                print('删除Cookies', username, flush=True)
        except ConnectionError as e:
            print('发生异常', e.args, flush=True)


class XiaohongshuValidTester(ValidTester):
    def __init__(self, website='xiaohongshu'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print('正在测试Cookies', '用户名', username, flush=True)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法', username, flush=True)
            self.cookies_db.delete(username)
            print('删除Cookies', username, flush=True)
            return
        try:

            test_url = TEST_URL_MAP[self.website]
            user_agent = user_agent_rotator.get_random_user_agent()
            proxy = proxy_wrapper_for_requests()

            response = requests.get(test_url, headers={
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'Referer': 'https://www.xiaohongshu.com/',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'User-Agent': user_agent, 'Referer': test_url}, proxies=proxy, cookies=cookies, timeout=5,
                                    allow_redirects=True)

            if response.status_code == 200:
                if response.text.find('datePublished') > -1:
                    print('Cookies有效', username, flush=True)
                else:
                    print('Cookies失效', username, flush=True)
                    self.cookies_db.delete(username)
                    print('删除Cookies', username, flush=True)

            else:
                print('Cookies失效', username, flush=True)
                self.cookies_db.delete(username)
                print('删除Cookies', username, flush=True)



        except ConnectionError as e:
            print('发生异常', e.args)


if __name__ == '__main__':
    XiaohongshuValidTester().run()

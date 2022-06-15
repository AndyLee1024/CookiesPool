import json
import uuid

import requests
from requests.exceptions import ConnectionError
from cookiespool.db import *
from cookiespool.libs import proxy_wrapper_for_requests, get_user_agent, generate_weixin_user_agent
from termcolor import colored


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
            print(colored(f'{self.website} 没有Cookies 无法进行测试', 'red'), flush=True)
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


class WeiboValidTester(ValidTester):
    def __init__(self, website='weibo'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print(colored('正在测试Cookies', 'red'), '用户名', username, flush=True)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法', username, flush=True)
            self.cookies_db.delete(username)
            print('删除Cookies', username, flush=True)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            proxy = proxy_wrapper_for_requests()
            response = requests.get(test_url, proxies=proxy, cookies=cookies, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                print(colored('Cookies有效', 'green'), username, flush=True)
            else:
                print('Cookies失效', username, flush=True)
                self.cookies_db.delete(username)
                print('删除Cookies', username, flush=True)
        except ConnectionError as e:
            print('发生异常', e.args, flush=True)


class XiaohongshuValidTester(ValidTester):
    def __init__(self, website='xiaohongshu'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print(colored('正在测试 xiaohongshu Cookies', 'yellow'), '用户名', username, flush=True)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法', username, flush=True)
            self.cookies_db.delete(username)
            print('删除Cookies', username, flush=True)
            return
        try:

            test_url = TEST_URL_MAP[self.website]
            proxy = proxy_wrapper_for_requests()

            response = requests.get(test_url, headers={
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'User-Agent': generate_weixin_user_agent(),
                'Referer': test_url}, proxies=proxy, cookies=cookies, timeout=5,
                                    allow_redirects=False)

            if response.status_code == 200:
                if response.text.find('generatedTitle') > -1:
                    print(colored('Cookies有效', 'green'), username, flush=True)
                else:
                    print('Cookies失效', username, flush=True)
                    self.cookies_db.delete(username)
                    print('删除Cookies', username, flush=True)
                    print(response.status_code, response.headers, flush=True)
            else:
                print('Cookies失效', username, flush=True)
                self.cookies_db.delete(username)
                print('删除Cookies', username, flush=True)

        except ConnectionError as e:
            print('发生异常', e.args, flush=True)


class BaijiahaoValidTester(ValidTester):
    def __init__(self, website='baijiahao'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print(colored('正在测试 baijiahao Cookies', 'yellow'), '用户名', username, flush=True)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法', username, flush=True)
            self.cookies_db.delete(username)
            print('删除Cookies', username, flush=True)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            proxy = proxy_wrapper_for_requests()
            response = requests.get(test_url, headers={
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'User-Agent': get_user_agent(),
                'Referer': test_url}, proxies=proxy, cookies=cookies, timeout=5,
                                    allow_redirects=False)
            if response.status_code == 200:
                if response.text.find('ssr-content-wrapper') > -1:
                    print(colored('Cookies有效', 'green'), username, flush=True)
                else:
                    print('Cookies失效', username, flush=True)
                    self.cookies_db.delete(username)
                    print('删除Cookies', username, flush=True)
                    print(response.status_code, response.headers, flush=True)
            else:
                print('Cookies失效', username, flush=True)
                self.cookies_db.delete(username)
                print('删除Cookies', username, flush=True)

        except ConnectionError as e:
            print('发生异常', e.args, flush=True)


class ZhihuValidTester(ValidTester):
    def __init__(self, website='zhihu'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        print(colored('正在测试 zhihu Cookies', 'yellow'), '用户名', username, flush=True)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法', username, flush=True)
            self.cookies_db.delete(username)
            print('删除Cookies', username, flush=True)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            proxy = proxy_wrapper_for_requests()
            response = requests.get(test_url, headers={
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'User-Agent': get_user_agent(),
                'Referer': test_url}, proxies=proxy, cookies=cookies, timeout=5,
                                    allow_redirects=False)
            if response.status_code == 200:
                if response.text.find('ssr-content-wrapper') > -1:
                    print(colored('Cookies有效', 'green'), username, flush=True)
                else:
                    print('Cookies失效', username, flush=True)
                    self.cookies_db.delete(username)
                    print('删除Cookies', username, flush=True)
                    print(response.status_code, response.headers, flush=True)
            else:
                print('Cookies失效', username, flush=True)
                self.cookies_db.delete(username)
                print('删除Cookies', username, flush=True)

        except ConnectionError as e:
            print('发生异常', e.args, flush=True)


if __name__ == '__main__':
    BaijiahaoValidTester().run()

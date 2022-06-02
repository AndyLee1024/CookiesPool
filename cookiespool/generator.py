import asyncio
import json
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from cookiespool.config import *
from cookiespool.db import RedisClient
from login.xiaohongshu.cookies import get_xiaohongshu_cookie


class CookiesGenerator(object):
    def __init__(self, website='default'):
        """
        父类, 初始化一些对象
        :param website: 名称
        :param browser: 浏览器, 若不使用浏览器则可设置为 None
        """
        self.browser = None
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)

    def new_cookies(self, username, password):
        """
        新生成Cookies，子类需要重写
        :param username: 用户名
        :param password: 密码
        :return:
        """
        raise NotImplementedError

    def process_cookies(self, cookies):
        """
        处理Cookies
        :param cookies:
        :return:
        """
        dict = {}
        for cookie in cookies:
            dict[cookie['name']] = cookie['value']
        return dict

    def run(self):
        """
        运行, 得到所有账户, 然后顺次模拟登录
        :return:
        """

        print(f'正在生成Cookies, Website is {self.website} browser type is {BROWSER_TYPE}')

        accounts_usernames = self.accounts_db.usernames()
        cookies_usernames = self.cookies_db.usernames()

        if len(accounts_usernames) == 0:
            print('没有账号密码，无法进行cookies 生成')
        else:
            for username in accounts_usernames:
                if not username in cookies_usernames:
                    password = self.accounts_db.get(username)
                    print('正在生成Cookies', '账号', username, '密码', password)
                    result = self.new_cookies(username, password)
                    # 成功获取
                    if result.get('status') == 1:
                        cookies = self.process_cookies(result.get('content'))
                        print('成功获取到Cookies', cookies)
                        if self.cookies_db.set(username, json.dumps(cookies)):
                            print('成功保存Cookies')
                    # 密码错误，移除账号
                    elif result.get('status') == 2:
                        if self.accounts_db.delete(username):
                            print('成功删除账号')
                    else:
                        print(result.get('content'))
            else:
                print('所有账号都已经成功获取Cookies')


class XiaohongshuCookiesGenerator(CookiesGenerator):
    def __init__(self, website='xiaohongshu'):
        """
        初始化操作
        :param website: 站点名称
        :param browser: 使用的浏览器
        """
        CookiesGenerator.__init__(self, website)
        self.website = website

    def new_cookies(self, username, password):
        """
        生成Cookies
        :param username: 用户名
        :param password: 密码
        :return: 用户名和Cookies
        """
        return asyncio.run(get_xiaohongshu_cookie(username, password))


if __name__ == '__main__':
    generator = XiaohongshuCookiesGenerator()
    generator.run()

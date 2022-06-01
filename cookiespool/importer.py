import uuid

import requests
import sys
from cookiespool.db import RedisClient
from cookiespool.config import *

'''
导入账号到 Cookies Pool
两种用法
1. python3 importer.py xiaohongshu  然后输入账号和密码
2. python3 importer.py xiaohongshu 30 系统将会随机生成账号，用于未登录cookie模式

'''

if len(sys.argv) < 2:
    raise ValueError('使用命令 python3 importer.py xiaohongshu')

conn = RedisClient('accounts', sys.argv[1])


def set(account, sep='----'):
    username, password = account.split(sep)
    result = conn.set(username, password)
    print('账号', username, '密码', password)
    print('录入成功' if result else '录入失败')


def scan():
    if len(sys.argv) > 2:
        go = input(f'使用自动填充模式，将会填充 {sys.argv[2]} 个账号。按下 任意键继续')
        for i in range(0, int(sys.argv[2])):
            set(f"{str(uuid.uuid1())}----{str(uuid.uuid1())}")
    else:
        print('请输入账号密码组, 每个一行，账号密码之间用 ---- 分割 输入exit退出读入')
        while True:
            account = input()
            if account == 'exit':
                break
            set(account)


if __name__ == '__main__':
    scan()

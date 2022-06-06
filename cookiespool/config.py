import os

# Redis数据库地址
REDIS_HOST = os.environ.get('REDIS_HOST', '124.220.177.240')

# 目前支持的平台类型

PLATFORM = ['weibo', 'xiaohongshu', 'toutiao', 'zhihu', 'baidu']

# Redis端口
REDIS_PORT = os.environ.get('REDIS_PORT', '33479')

# Redis密码，如无填None
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', 'eYVX7mxKPCDmwMtyKVge8oLd2t81')

# 产生器使用的浏览器
BROWSER_TYPE = 'Chromium'

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {
    'xiaohongshu': 'XiaohongshuCookiesGenerator',
}

# 测试类，如扩展其他站点，请在此配置
TESTER_MAP = {
    'xiaohongshu': 'XiaohongshuValidTester'
}

PROXY_POOL_URL = os.environ.get('PROXY_POOL_ADDRESS', 'http://124.220.177.240:8425/random')

TEST_URL_MAP = {
    'xiaohongshu': 'https://www.xiaohongshu.com/discovery/item/628b664800000000010263f5'
}

# 产生器和验证器循环周期
CYCLE = 120

# API地址和端口
API_HOST = '0.0.0.0'
API_PORT = 5022

# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = False
# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = True
# API接口服务
API_PROCESS = True

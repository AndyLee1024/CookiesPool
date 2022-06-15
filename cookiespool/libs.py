import requests
from cookiespool.config import PROXY_POOL_URL
import uuid
import mimetypes
import random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import base64
import hashlib

def x96_b64encode(in_put: str) -> str:
    in_put = in_put.encode('utf-8')
    while len(in_put) % 3 != 0:
        in_put += bytes([0])

    table1 = list('RuPtXwxpThIZ0qyz_9fYLCOV8B1mMGKs7UnFHgN3iDaWAJE-Qrk2ecSo6bjd4vl5')
    table2 = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/')
    table3 = {table2[v]: table1[v] for v in range(len(table1))}

    b64_in = bytearray()
    for i in range(len(in_put) - 1, 0, -3):
        b64_in += in_put[i - 2: i + 1]
    for i in range(0, len(b64_in), 12):
        b64_in[i + 2], b64_in[i + 4], b64_in[i + 6] = b64_in[i + 2] ^ 42, b64_in[i + 4] ^ 42, b64_in[i + 6] ^ 42

    b64_out = ''.join(list(map(lambda n: table3[n], list(base64.b64encode(b64_in).decode()))))
    return ''.join([b64_out[i: i + 4][::-1] for i in range(0, len(b64_out), 4)])


def get_user_agent():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    return user_agent_rotator.get_random_user_agent()


def generate_weixin_user_agent():
    iOS_version_random = random.randint(12, 15)
    android_version_random = random.randint(8, 12)

    uas = [
        f'Mozilla/5.0 (Linux; Android {android_version_random}; RMX3115 Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3225 MMWEBSDK/20220402 Mobile Safari/537.36 MMWEBID/7093 MicroMessenger/8.0.22.2140(0x2800{android_version_random}E6) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
        f'Mozilla/5.0 (iPhone; CPU iPhone OS {iOS_version_random}_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/{iOS_version_random}E148 MicroMessenger/8.0.22(0x1800{iOS_version_random}28) NetType/WIFI Language/zh_CN',
        f'Mozilla/5.0 (Linux; Android {android_version_random}; M2007J1SC Build/QKQ1.200419.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3225 MMWEBSDK/20220402 Mobile Safari/537.36 MMWEBID/2728 MicroMessenger/8.0.22.2140(0x2800{android_version_random}F2) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64'
    ]
    return random.choice(uas)


def get_random_proxy():
    """
    :return: proxy
    """
    proxy = requests.get(PROXY_POOL_URL).text.strip()
    print('http://{}'.format(proxy))
    return proxy


def download_image(url):
    response = requests.get(url, headers={'Referer': 'https://www.xiaohongshu.com/',
                                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'},
                            )
    content_type = response.headers['content-type']
    extension = mimetypes.guess_extension(content_type)
    name = str(uuid.uuid1())
    filename = '{}{}'.format(name, extension)
    with open(filename, 'wb') as out_file:
        out_file.write(response.content)
    return filename


def get_trajectory_1(distance):
    ge = [[0, 0, 0]]
    for i in range(10):
        x = 0
        y = random.randint(-1, 1)
        t = 100 * (i + 1) + random.randint(0, 2)
        ge.append([x, y, t])
    for items in ge[1:-5]:
        items[0] = distance // 2
    for items in ge[-5:-1]:
        items[0] = distance + random.randint(1, 4)
    ge[-1][0] = distance
    return ge, ge[-1][2]


def proxy_wrapper_for_requests():
    proxy = get_random_proxy()
    return {
        "http": f'http://{proxy}',
        "https": f'http://{proxy}'
    }

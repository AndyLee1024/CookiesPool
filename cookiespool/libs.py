import requests
from cookiespool.config import PROXY_POOL_URL
import uuid
import mimetypes
import shutil
import random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def get_user_agent(number):
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=number)

    if number <= 1:
        return user_agent_rotator.get_random_user_agent()
    else:
        return user_agent_rotator.get_user_agents()


def get_random_proxy():
    """
    :return: proxy
    """
    proxy = requests.get(PROXY_POOL_URL).text.strip()
    print('http://{}'.format(proxy))
    return proxy


def download_image(url):
    response = requests.get(url, stream=True)
    content_type = response.headers['content-type']
    extension = mimetypes.guess_extension(content_type)
    name = str(uuid.uuid1())
    filename = '{}.{}'.format(name, extension)
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
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
        "http": proxy,
        "https": proxy
    }

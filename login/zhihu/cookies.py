import aiohttp
import asyncio
import time

from cookiespool.config import PROXY_POOL_URL, TEST_URL_MAP
from cookiespool.libs import get_user_agent


async def get_zhihu_cookie():
    headers = {
        "referer": "https://www.zhihu.com/search?type=content&q=python&utm_content=search_preset",
        "user-agent": get_user_agent(),
    }
    async with aiohttp.ClientSession() as session:
        # proxy = await get_random_proxy()
        # async with session.post(TEST_URL_MAP.get('zhihu'), headers=headers,proxy=proxy) as res:
        async with session.post(TEST_URL_MAP.get('zhihu'), headers=headers) as res:
            text = await res.text(encoding='utf-8')
            stmp = int(time.time())
            dc0 = f'd_c0="{text}=|{stmp}";'
            print(dc0)
            return dc0


async def get_random_proxy():
    async with aiohttp.ClientSession() as session:
        async with session.get(PROXY_POOL_URL) as res:
            text = await res.text(encoding='utf-8')
            return {
                'http': text.strip()
            }


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_zhihu_cookie())

import asyncio
import os
import time
import hashlib
import uuid

from pyppeteer import launch
from cookiespool.libs import get_random_proxy, generate_weixin_user_agent
from cookiespool.config import TEST_URL_MAP

HIDE_WEBDRIVER = '''() => {Object.defineProperty(navigator, 'webdriver', {get: () => undefined})}'''
SET_USER_AGENT = '''() => {Object.defineProperty(navigator, 'userAgent', {get: () => '%s'})}'''
SET_APP_VERSION = '''() => {Object.defineProperty(navigator, 'appVersion', {get: () => '5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})}'''
EXTEND_LANGUAGES = '''() => {Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en', 'zh-TW', 'ja']})}'''
EXTEND_PLUGINS = '''() => {Object.defineProperty(navigator, 'plugins', {get: () => [0, 1, 2, 3, 4]})}'''
EXTEND_MIME_TYPES = '''() => {Object.defineProperty(navigator, 'mimeTypes', {get: () => [0, 1, 2, 3, 4]})}'''
CHANGE_WEBGL = '''() => {
    const getParameter = WebGLRenderingContext.getParameter
    WebGLRenderingContext.prototype.getParameter = (parameter) => {
      if (parameter === 37445) {
        return 'Intel Open Source Technology Center'
      }
      if (parameter === 37446) {
        return 'Mesa DRI Intel(R) Ivybridge Mobile '
      }
      return getParameter(parameter)
    }
  }
'''
SET_CHROME_INFO = '''() => {
  Object.defineProperty(window, 'chrome', {
    "app": {
      "isInstalled": false,
      "InstallState": {"DISABLED": "disabled", "INSTALLED": "installed", "NOT_INSTALLED": "not_installed"},
      "RunningState": {"CANNOT_RUN": "cannot_run", "READY_TO_RUN": "ready_to_run", "RUNNING": "running"}
    },
    "runtime": {
      "OnInstalledReason": {
        "CHROME_UPDATE": "chrome_update",
        "INSTALL": "install",
        "SHARED_MODULE_UPDATE": "shared_module_update",
        "UPDATE": "update"
      },
      "OnRestartRequiredReason": {"APP_UPDATE": "app_update", "OS_UPDATE": "os_update", "PERIODIC": "periodic"},
      "PlatformArch": {
        "ARM": "arm",
        "ARM64": "arm64",
        "MIPS": "mips",
        "MIPS64": "mips64",
        "X86_32": "x86-32",
        "X86_64": "x86-64"
      },
      "PlatformNaclArch": {"ARM": "arm", "MIPS": "mips", "MIPS64": "mips64", "X86_32": "x86-32", "X86_64": "x86-64"},
      "PlatformOs": {
        "ANDROID": "android",
        "CROS": "cros",
        "LINUX": "linux",
        "MAC": "mac",
        "OPENBSD": "openbsd",
        "WIN": "win"
      },
      "RequestUpdateCheckStatus": {
        "NO_UPDATE": "no_update",
        "THROTTLED": "throttled",
        "UPDATE_AVAILABLE": "update_available"
      }
    }
  })
}
'''

CHANGE_PERMISSION = '''() => {
  const originalQuery = window.navigator.permissions.query;
  return window.navigator.permissions.query = (parameters) => (
    parameters.name === 'notifications' ?
      Promise.resolve({ state: Notification.permission }) :
      originalQuery(parameters)
  )
}
'''


async def get_baijiahao_cookie(username, password):
    result = {
        'status': 3
    }
    browser = await launch(headless=False, defaultViewport=None,
                           ignoreDefaultArgs=[
                               '--enable-automation'
                           ],
                           args=['--disable-infobars',
                                 '--no-sandbox',
                                 '--disable-setuid-sandbox',
                                 '--password-store=basic',
                                 '--account-consistency',
                                 '--aggressive',
                                 '--proxy-server={}'.format(get_random_proxy()),
                                 '--allow-running-insecure-content',
                                 '--allow-no-sandbox-job',
                                 '--allow-outdated-plugins',
                                 '--disable-gpu'])
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()
    try:
        await page.evaluateOnNewDocument(HIDE_WEBDRIVER)
        await page.evaluateOnNewDocument(EXTEND_LANGUAGES)
        await page.evaluateOnNewDocument(EXTEND_PLUGINS)
        await page.evaluateOnNewDocument(EXTEND_MIME_TYPES)
        await page.evaluateOnNewDocument(CHANGE_WEBGL)
        await page.evaluateOnNewDocument(SET_CHROME_INFO)
        await page.evaluateOnNewDocument(CHANGE_PERMISSION)

        await page.emulate(
            options={'viewport': {'width': 390, 'height': 844, 'isMobile': True},
                     'userAgent': generate_weixin_user_agent()})

        uuid_md5 = hashlib.md5(str(uuid.uuid1()).encode()).hexdigest()
        url = TEST_URL_MAP.get('baijiahao').format(uuid_md5)
        await page.goto(url)
        print('testing url -> {}'.format(url))
        current_url = page.url
        if current_url.find('wappass') == -1:
            result['status'] = 1
            result['content'] = await page.cookies()

        print('Successful to get cookies', result)
    finally:
        await browser.close()
        return result



if __name__ == '__main__':
    asyncio.run(get_baijiahao_cookie('test', 'test'))

import asyncio
import os
import time

from pyppeteer import launch
import ddddocr
import random
from cookiespool.libs import get_random_proxy, download_image, get_trajectory_1, generate_weixin_user_agent
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


async def get_xiaohongshu_cookie(username, password):
    result = {
        'status': 3
    }

    browser = await launch(headless=True, defaultViewport=None,
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
    try:
        context = await browser.createIncognitoBrowserContext()
        page = await context.newPage()
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
        await page.goto(TEST_URL_MAP.get('xiaohongshu').format(int(time.time())))

        for i in range(0, 2):
            print(page.url)
            await asyncio.sleep(4)

            captcha = await page.querySelector('.shumei_captcha_loaded_img_bg')

            print(f'captcha status {captcha}')
            if captcha is None:
                break
            else:
                await slide(page, captcha)
                await asyncio.sleep(3)

        current_url = page.url

        if current_url.find('captcha') == -1:
            result['status'] = 1
            result['content'] = await page.cookies()

    except Exception as err:
        print('got exception {}'.format(err), flush=True)
    finally:
        await browser.close()
        print('Successful to get cookies', result)
        return result


async def slide(pageObject, captchaObject):
    page = pageObject
    background_src = await page.evaluate('(captcha) => captcha.getAttribute("src")', captchaObject)
    target = await page.J('.shumei_captcha_loaded_img_fg')
    target_src = await page.evaluate('(target) => target.getAttribute("src")', target)
    print('发现验证码', background_src, target_src)
    if background_src is not None and target_src is not None:
        background_image = download_image(background_src)
        target_image = download_image(target_src)
        det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)

        with open(target_image, 'rb') as f:
            target_bytes = f.read()

        with open(background_image, 'rb') as f:
            background_bytes = f.read()

        res = det.slide_match(target_bytes, background_bytes)

        os.remove(target_image)
        os.remove(background_image)

        btn = await page.J('.shumei_captcha_slide_btn')
        handle = await btn.boundingBox()

        handleX = handle.get('x') + handle.get('width') / 2
        handleY = handle.get('y') + handle.get('height') / 2
        await asyncio.sleep(random.uniform(0.1, 0.6))

        random_zoom = random.uniform(0.666666, 0.6666)
        x = (res.get('target')[0]) * random_zoom
        trajectories = get_trajectory_1(x)

        await page.mouse.move(handleX, handleY)
        await page.mouse.down()

        for trajectory in trajectories[0]:
            print(trajectory[0] + handleX, trajectory[1] + handleY, trajectory[2])
            await page.mouse.move(trajectory[0] + handleX, trajectory[1] + handleY,
                                  options={'steps': random.randint(10, 30)})
        await page.mouse.up()
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(get_xiaohongshu_cookie('test', 'test'))

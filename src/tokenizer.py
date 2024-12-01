import re
import time
from playwright.sync_api import sync_playwright
from .config import Config

pw = None


def parse_url(url: str) -> str:
    pattern = 'https://oauth.vk.com/blank.html#access_token=(.+)&user_id=(.+)'
    if (m := re.fullmatch(pattern, url)):
        return m.group(1)


def check_url(url: str) -> bool:
    return url.startswith('https://oauth.vk.com/blank.html#access_token=')


def get_pw():
    global pw
    if pw is None:
        pw = sync_playwright().start()
    return pw


def get_page():
    playwright = get_pw()
    browser = playwright.chromium.launch(
        headless=False,
        channel='chrome'
    )
    page = browser.new_page()
    return page


def get_captcha(img_captcha: str) -> str:
    page = get_page()
    page.goto(img_captcha)
    code = input('Enter captcha code: ')
    page.close()
    return code


def get_token(config: Config):
    page = get_page()
    page.goto(
        'https://oauth.vk.com/authorize?client_id=2685278&scope=140492255&response_type=token')

    page.wait_for_selector('//input[@name="login"]')
    page.fill('//input[@name="login"]', config.phone[:-1], force=True)
    time.sleep(1)
    page.fill('//input[@name="login"]', config.phone, force=True)
    time.sleep(1)
    page.click('//button[@type="submit"]')

    page.fill('//input[@name="password"]', config.password)
    page.click('//button[@type="submit"]')

    if 'id.vk.com' in page.url:
        code = input("Enter 2FA Code: ")
        page.fill('//input[@name="otp"]', code)
        page.click('//button[@type="submit"]')

    page.wait_for_url(check_url)
    page.close()
    page.context.close()

    token = parse_url(page.url)
    config.token = token
    config.dump()
    return token


if __name__ == '__main__':
    print(get_token(input('Enter phone: '),
                    input('Enter password: ')))

import re
from playwright.sync_api import sync_playwright
from .config import Config


def parse_url(url: str) -> str:
    pattern = 'https://oauth.vk.com/blank.html#access_token=(.+)&user_id=(.+)'
    if (m := re.fullmatch(pattern, url)):
        return m.group(1)


def check_url(url: str) -> bool:
    return url.startswith('https://oauth.vk.com/blank.html#access_token=')


def get_page(config: Config):
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=False,
        channel='chrome'
    )
    page = browser.new_page()
    return page


def get_token(config: Config):
    page = get_page(config)
    page.goto(
        'https://oauth.vk.com/authorize?client_id=2685278&scope=140492255&response_type=token')

    page.fill('//input[@name="login"]', config.phone)
    page.click('//button[@type="submit"]')

    page.fill('//input[@name="password"]', config.password)
    page.click('//button[@type="submit"]')

    code = input("Enter 2FA Code: ")
    page.fill('//input[@name="otp"]', code)
    page.click('//button[@type="submit"]')

    page.wait_for_url(check_url)
    page.close()

    token = parse_url(page.url)
    config.token = token
    config.dump()
    return token


if __name__ == '__main__':
    print(get_token(input('Enter phone: '),
                    input('Enter password: ')))

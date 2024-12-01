import yaml
import vk_api
from vk_api import ApiError, Captcha

with open('config.yaml', 'rb') as f:
    data = yaml.safe_load(f)
    token = data['token']


vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()


def send_captcha(exc: Captcha) -> dict:
    code = input(exc.get_url()+'  : ')
    return exc.try_again(code)


def send(**kwargs):
    try:
        d = vk.captcha.force(uid=66748, **kwargs)
    except Captcha as exc:
        exc.url
        return
    print(d)


send()

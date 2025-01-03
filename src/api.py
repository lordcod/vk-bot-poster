import vk_api
import time
from functools import cached_property
from datetime import datetime
from vk_api import VkUpload, ApiError, Captcha
from loguru import logger
from .tokenizer import get_captcha


class WallPosterApi:
    def __init__(self, token: str, group_id: str):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self._group_id = group_id

    @cached_property
    def group_id(self) -> int:
        group = self.vk.groups.get_by_id(
            group_id=self._group_id, fields=['can_post'])[0]

        logger.info(f"Logged into the {group['name']} group")
        if group['is_closed'] == 1:
            raise TypeError("Empty community")
        if not group['can_post']:
            raise TypeError(
                "There is no way to create an api in the community")
        return group['id']

    def is_valid(self) -> bool:
        try:
            data = self.vk.account.get_info()
        except ApiError as exc:
            logger.exception(f'{type(exc).__name__}: {exc}')
            return False
        else:
            logger.info(f'The account is connected: {data}')
            return True

    def upload_photo(self, filename: str) -> dict:
        try:
            upload = VkUpload(self.vk_session)
            photo = upload.photo_wall(photos=filename)[0]
        except Exception:
            logger.warning("The delay is set to 10 seconds")
            time.sleep(10)
            return self.upload_photo(filename)
        return photo

    def send_captcha(self, exc: Captcha, code: str | None = None) -> dict:
        logger.warning("Waiting for a captcha!")
        if code is None:
            code = get_captcha(exc.get_url())
        try:
            return exc.try_again(code)
        except ApiError:
            logger.warning("The delay is set to 10 seconds")
            time.sleep(10)
            return self.send_captcha(exc, code)
        except Captcha as exc:
            logger.warning("Incorrect captcha!")
            return self.send_captcha(exc)

    def post_wall(self, datetime: datetime, text: str, filename: str):
        photo = self.upload_photo(filename)
        try:
            post = self.vk.wall.post(
                message=text,
                primary_attachments='photo{}_{}_{}'.format(
                    photo['owner_id'], photo['id'], photo['access_key']),
                primary_attachments_mode="carousel",
                owner_id=f'-{self.group_id}',
                signed=0,
                from_group=1,
                ref="group_from_plus",
                entry_point="group",
                publish_date=int(datetime.timestamp())
            )
        except Captcha as exc:
            return self.send_captcha(exc)
        except ApiError as exc:
            logger.exception(f'Api Error {exc.error}')
            return
        return post

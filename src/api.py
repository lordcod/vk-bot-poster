import vk_api
import os
from vk_api import VkUpload


class WallPosterApi:
    def __init__(self, token: str, group_id: int):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self.group_id = group_id

    def upload_photo(self, filename: str) -> dict:
        upload = VkUpload(self.vk_session)
        photo = upload.photo_wall(photos=filename)[0]
        return photo

    def post_wall(self, text: str, filename: str) -> int:
        photo = self.upload_photo(filename)
        post = self.vk.wall.post(
            message=text,
            primary_attachments='photo{}_{}_{}'.format(
                photo['owner_id'], photo['id'], photo['access_key']),
            primary_attachments_mode="carousel",
            owner_id=f'-{self.group_id}',
            signed=0,
            from_group=1,
            ref="group_from_plus",
            entry_point="group"
        )
        return post['post_id']

import vk_api
from datetime import datetime
from vk_api import VkUpload, ApiError


class WallPosterApi:
    def __init__(self, token: str, group_id: int):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self.group_id = group_id

    def is_valid(self) -> bool:
        try:
            self.vk.account.get_info()
        except ApiError:
            return False
        else:
            return True

    def upload_photo(self, filename: str) -> dict:
        upload = VkUpload(self.vk_session)
        photo = upload.photo_wall(photos=filename)[0]
        return photo

    def get_time(self) -> None:
        pass

    def post_wall(self, datetime: datetime, text: str, filename: str) -> int:
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
            entry_point="group",
            publish_date=int(datetime.timestamp())
        )
        return post['post_id']

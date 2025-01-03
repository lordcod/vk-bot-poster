import os
from datetime import datetime, timedelta
from loguru import logger
from .api import WallPosterApi
from .config import Config, IMAGES_PATH


def get_sender(wpa: WallPosterApi, msg: str):
    def send(datetime: datetime, image: str):
        logger.info(f'Send post {msg}: {image}')
        wpa.post_wall(datetime, msg, image)
    return send


def main():
    config = Config.load()

    wpa = WallPosterApi(config.token, config.group_id)
    if not wpa.is_valid():
        config.reload_token(True)
        wpa = WallPosterApi(config.token, config.group_id)

    today = datetime.today()
    time_now = datetime(
        today.year,
        today.month,
        today.day,
        config.hour,
        config.minute
    )
    send = get_sender(wpa, config.message)
    files = os.listdir(IMAGES_PATH)
    files.sort(key=lambda item: item.split('.')[0])
    for i, filename in enumerate(files, start=1):
        path = os.path.join(IMAGES_PATH, str(i)+'.'+filename.split('.')[-1])
        send(time_now + timedelta(days=i), path)
    logger.warning("The images are over!")

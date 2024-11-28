import os
import time
from datetime import datetime
from loguru import logger
from .api import WallPosterApi
from .config import Config

IMAGES_PATH = os.path.join(os.getcwd(), 'images')


def get_sender(wpa: WallPosterApi, msg: str):
    def send(image: str):
        logger.info(f'Send post {msg}: {image}')
        wpa.post_wall(msg, image)
    return send


def check_time(hour, minute, last: datetime):
    hour, minute = int(hour), int(minute)
    today = datetime.today()
    if (
        today.hour >= hour
        and hour >= last.hour
        and today.minute >= minute
        and minute >= last.minute
    ):
        return True, None
    return False, today


def wait_for(hour, minute, delay):
    last = datetime.today()
    logger.info(f'Start shipping! Sending in {hour}:{minute}')
    while True:
        logger.debug("Check time")
        result, last = check_time(hour, minute, last)
        if result:
            return
        time.sleep(delay)


def accept():
    enter = input('Send a message? (y/n)')
    if enter == 'y':
        return True
    elif enter == 'n':
        return False
    else:
        return accept()


def main():
    config = Config.load()
    wpa = WallPosterApi(config.token, config.group_id)
    send = get_sender(wpa, config.message)
    for i, filename in enumerate(os.listdir(IMAGES_PATH)):
        if i >= 50:
            if not accept():
                return
        wait_for(config.hour, config.minute, config.delay)
        path = os.path.join(IMAGES_PATH, filename)
        send(path)
    logger.warning("The images are over!")

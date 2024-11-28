import os
import time
from datetime import datetime
from loguru import logger
from .api import WallPosterApi
from .config import Config, IMAGES_PATH


last_sended_time = None


def get_sender(wpa: WallPosterApi, msg: str):
    def send(image: str):
        global last_sended_time
        logger.info(f'Send post {msg}: {image}')
        wpa.post_wall(msg, image)
        last_sended_time = datetime.today()
    return send


def check_time(hour, minute, last: datetime):
    hour, minute = int(hour), int(minute)
    today = datetime.today()
    if (
        today.hour >= hour
        and hour >= last.hour
        and today.minute >= minute
        and minute >= last.minute
        and (not last_sended_time
             or (today-last_sended_time).total_seconds() >= 60)
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
    files = os.listdir(IMAGES_PATH)
    for i, filename in enumerate(files):
        if i >= 50:
            if not accept():
                return
        wait_for(config.hour, config.minute, config.delay)
        path = os.path.join(IMAGES_PATH, filename)
        send(path)
        # if len(files) > i:
        #     logger.debug("One minute delay!")
        #     time.sleep(60)
    logger.warning("The images are over!")

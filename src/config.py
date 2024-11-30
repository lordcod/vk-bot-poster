from dataclasses import dataclass
import yaml
import os
from pathlib import Path

PARENT_PATH = Path(__file__).parent.parent
CONFIG_PATH = os.path.join(PARENT_PATH, 'config.yaml')
IMAGES_PATH = os.path.join(PARENT_PATH, 'images')


def deploy_token(data: 'Config', reload: bool = False):
    from .tokenizer import get_token
    if data.token and not reload:
        return data.token
    return get_token(data)


@dataclass
class Config:
    data: dict
    token: str
    message: str
    group_id: int
    phone: str
    password: str
    hour: int
    minute: int
    delay: int

    def __post_init__(self):
        self.reload_token()

    def reload_token(self, reload: bool = False):
        self.token = deploy_token(self, reload)

    def dump(self):
        return
        with open(CONFIG_PATH, 'w+') as file:
            yaml.safe_dump(self.data, file)

    @classmethod
    def load(cls) -> 'Config':
        try:
            with open(CONFIG_PATH, 'rb+') as file:
                data = yaml.safe_load(file)
        except Exception:
            data = {}

        message = str(data.get('message')) or input('Enter message: ')
        group_id = str(data.get('group_id') or input('Enter group id: '))
        phone = str(data.get('phone', '')) or input('Enter phone: ')
        password = str(
            data.get('password', '')) or input('Enter password: ')
        hour, minute = list(map(int, (data.get('date') or input(
            'Enter date (12:00): ')).split(':')))
        delay = int(data.get('delay') or input('Enter delay: '))
        return cls(
            data,
            data.get('token'),
            message,
            group_id,
            phone,
            password,
            hour,
            minute,
            delay,
        )

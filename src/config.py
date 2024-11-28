from dataclasses import dataclass
import yaml
import os
from .tokenizer import get_token


CONFIG_PATH = os.path.join(os.getcwd(), 'config.yaml')


def deploy_token(data: dict):
    token = data.get('token')
    if token:
        return token

    phone, password = str(data.get('phone', '')), str(data.get('password', ''))
    if not phone:
        phone = input('Enter phone: ')
    if not password:
        password = input('Enter password: ')
    return get_token(phone, password)


@dataclass
class Config:
    token: str
    message: str
    group_id: int
    hour: int
    minute: int
    delay: int

    @classmethod
    def load(cls) -> 'Config':
        try:
            with open(CONFIG_PATH, 'rb+') as file:
                data = yaml.safe_load(file)
        except Exception:
            data = {}
        
        message = str(data.get('message')) or input('Enter message: ')
        group_id = int(data.get('group_id') or input('Enter group id: '))
        hour, minute = (data.get('date') or input(
            'Enter date (12:00): ')).split(':')
        delay = int(data.get('delay') or input('Enter delay: '))
        return cls(
            deploy_token(data),
            message,
            group_id,
            hour,
            minute,
            delay
        )

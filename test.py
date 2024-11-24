import os
from src.api import WallPosterApi
from dotenv import load_dotenv
load_dotenv()


wpa = WallPosterApi(os.getenv('token'), os.getenv('group_id'))
wpa.post_wall("", "images/image.png")

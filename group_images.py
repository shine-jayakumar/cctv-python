
# group_images.py
# groups images as per the date/time

import time
from modules.helpers import group_images
from constants.constants import GROUP_IMAGES_INTERVAL


st = time.time()
while True:
    en = time.time()
    if en - st >= GROUP_IMAGES_INTERVAL:
        group_images()
        st = en
        
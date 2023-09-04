import time
from modules.helpers import group_images


st = time.time()
while True:
    en = time.time()
    if en - st >= 2:
        group_images()
        st = en
        
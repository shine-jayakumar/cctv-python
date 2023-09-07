
# constants.py
# contains constants used in the script

import os


IMG_PATH = os.path.join(os.getcwd(), 'static/img')
APPIMGS_PATH = os.path.join(os.getcwd(), 'static/img/appimgs')

ERROR404_IMG_PATH = os.path.join(APPIMGS_PATH, 'error-404.png')


IMGCAP_INTERVAL = 0.2
MAX_IMGCAP_ERROR_THRESHOLD = 20

GROUP_IMAGES_INTERVAL = 2

DEFAULT_FONT = os.path.join(os.getcwd(), 'fonts/Ubuntu-R.ttf')

STREAM_INTERVAL = {
    'normal': 0.3,
    'slow': 0.4,
    'fast': 0.1
}

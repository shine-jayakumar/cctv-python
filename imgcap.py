
# imgcap.py
# Image capture script to save images from camera


import cv2
import sys
import os
import time
from datetime import datetime
from modules.applogger import AppLogger
from constants.constants import IMG_PATH, IMGCAP_INTERVAL


log = AppLogger('IMAGE_CAPTURE').getlogger()

log.info('ImgCap started')

cap = None
try:
    log.info('Initiating camera')
    cap = cv2.VideoCapture(0)
    log.info('Camera initiated')
except Exception as ex:
    log.error(f'Error initiating camera: {ex.__class__.__name__} - {str(ex)}')
    sys.exit(1)

st = time.time()

log.info(f'Image capturing started with interval: {IMGCAP_INTERVAL} seconds')
while True:

    ret,frame = (None, None)
    try:
        ret,frame = cap.read()
    except Exception as ex:
        log.error(f'Camera Read Error: {ex.__class__.__name__} - {str(ex)}')
        sys.exit(1)

    if not ret:
        log.error('Error while reading from camera')
        sys.exit(2)
        
    # IMG_PATH/20230910_075003688260.jpg
    img_name = os.path.join(IMG_PATH, f"{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.jpg")
    try:
        cv2.imwrite(img_name, frame)
    except Exception as ex:
        log.error(f'[Write error] Image file: {img_name}')

    time.sleep(IMGCAP_INTERVAL)





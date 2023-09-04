
# imgcap.py
# Image capture script to save images from camera


import cv2
import sys
import os
import time
from datetime import datetime
from modules.applogger import AppLogger
from constants.constants import IMG_PATH


log = AppLogger('IMAGE_CAPTURE').getlogger()

log.info('captureframes started')

cap = None
try:
    log.info('Initiating camera')
    cap = cv2.VideoCapture(0)
except Exception as ex:
    log.error(f'Error initiating camera: {ex.__class__.__name__} - {str(ex)}')
    sys.exit(1)

st = time.time()

log.info('Reading images from camera')
while True:

    ret,frame = (None, None)
    try:
        ret,frame = cap.read()
    except Exception as ex:
        log.error(f'Camera Read Error: {ex.__class__.__name__} - {str(ex)}')
        break

    if not ret:
        log.error('Error while reading from camera')
        break
    
    img_name = os.path.join(IMG_PATH, f"{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.jpg")
    cv2.imwrite(img_name, frame)
    time.sleep(0.2)





import cv2
import time

cap = cv2.VideoCapture(0)

output = cv2.VideoWriter('testvideo.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         20,
                         (640,480))

st = time.time()

while True:
    ret,frame = cap.read()
    output.write(frame)

    en = time.time()
    if en - st >= 5:
        break

cap.release()
output.release()


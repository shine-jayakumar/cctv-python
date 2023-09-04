
from flask import Flask, render_template, Response, request, send_file
from constants.constants import ERROR404_IMG_PATH
from modules.helpers import get_images
from modules.applogger import AppLogger
import time
import os


app = Flask(__name__)

log = AppLogger('VIDEO_STREAM').getlogger()


# def genframe():
#     camera = cv2.VideoCapture(0)
#     while True:

#         success,frame = camera.read()
#         if not success:
#             break

#         ret,buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()

#         yield(b'--frame\r\n'
#               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def stream_images(images: list[str], delay: int = 0.3):
    """
    Streams list of images
    """
    if not images:
        return b''

    for img in images:

        imgdata = b''
        with open(img, 'rb') as imgfh:
            imgdata = imgfh.read()
        
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n'+ imgdata + b'\r\n'
        )
        time.sleep(delay)
        

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/stream', methods=['GET', 'POST'])
def stream():
    if not request.args:
        log.info('No parameters specified for /video route')
        return send_file(ERROR404_IMG_PATH, mimetype='image/png')
    
    imgdate = request.args.get('imgdate', '')
    time_st = request.args.get('time_st', '')
    time_en = request.args.get('time_en', '')

    if not all([imgdate, time_st, time_en]):
        log.info('Either image date, start, end time missing')
        return send_file(ERROR404_IMG_PATH, mimetype='image/png')
    
    images = get_images(
        imgdate = imgdate,
        time_st = time_st,
        time_en = time_en
    )
    if not images:
        return send_file(ERROR404_IMG_PATH, mimetype='image/png')
    
    return Response(
        stream_images(images=images),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=2121)


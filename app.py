
# app.py
# main script called by gunicorn
# registers endpoints


from flask import Flask, render_template, Response, request, send_file
from constants.constants import ERROR404_IMG_PATH, STREAM_INTERVAL
from modules.helpers import get_images, stream_images
from modules.applogger import AppLogger


app = Flask(__name__)

log = AppLogger('VIDEO_STREAM').getlogger()
  

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# stream endpoint
# fetches and streams images
@app.route('/stream', methods=['GET', 'POST'])
def stream():

    # if image date and time range is not specified
    if not request.args:
        log.info('No parameters specified for /video route')
        return send_file(ERROR404_IMG_PATH, mimetype='image/png')
    
    imgdate = request.args.get('imgdate', '')
    time_st = request.args.get('time_st', '')
    time_en = request.args.get('time_en', '')
    delay = STREAM_INTERVAL.get(request.args.get('speed', 'normal'))

    if not all([imgdate, time_st, time_en]):
        log.info('[{imgdate=} {time_st=} {time_en=}] Either image date, start, end time is missing')
        return send_file(ERROR404_IMG_PATH, mimetype='image/png')
    
    # fetch list of images to stream
    images = get_images(
        imgdate = imgdate,
        time_st = time_st,
        time_en = time_en
    )
    log.info(f'[{imgdate=} {time_st=} {time_en=}] Total images: {len(images)}')
    if not images:
        log.info(f'[{imgdate=} {time_st=} {time_en=}] No images found for the date range')
        return send_file(ERROR404_IMG_PATH, mimetype='image/png')
    
    # stream images
    return Response(
        stream_images(images=images, delay=delay),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=2121)


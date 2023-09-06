from flask import Flask, Response
import cv2

app = Flask(__name__)

cap = cv2.VideoCapture(0)


def get_stream():

    while True:
        status,frame = cap.read()
        if not status:
            break
        ret,buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n'+ frame + b'\r\n'
        )

@app.route('/')
def streamlive():

    return Response(get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=2121)
    

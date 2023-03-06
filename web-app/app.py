from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import cv2
from Controller import Controller
from Connection import Connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#camera = cv2.VideoCapture(0)

controller = Controller()
#connection = Connection()

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('controller')
def handle_controller_input(data):
    global controller

    x = data['x2']
    y = data['y2']
    
    if x >= -1 and x <= 1 and y >= -1 and y <= 1:
        print("x: %f\ty: %f" % (x, y))
        controller.update_position(x, y)

if __name__ == '__main__':
    socketio.run(app)


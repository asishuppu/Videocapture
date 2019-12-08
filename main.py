import cv2
from flask import Flask, render_template, Response
from camera import VideoCamera
import time
import datetime
import os
import shutil
app = Flask(__name__, static_url_path = "/images/", static_folder = "images")
@app.route('/')
def index():
    return render_template('index.html')
def capture():
    return render_template('capture.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def vcapture(camera,imgname):
    frame = camera.get_image()
    if os.path.exists("images"):
        shutil.rmtree("images")
    os.mkdir("images")
    file = "images/"+imgname
    cv2.imwrite(file, frame)
    camera.delete()
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture',methods=['GET', 'POST'])
def capture():
    t=time.localtime()
    d= datetime.date.today()
    ctime=time.strftime("%H_%M_%S",t)
    iname=str(d)+"-"+str(ctime)+".jpg"
    vcapture(VideoCamera(),iname)
    return render_template('capture.html',imgname=iname)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

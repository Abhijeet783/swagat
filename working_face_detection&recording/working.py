import cv2
import time
from flask import Flask, Response,render_template, url_for, redirect,request
import pyaudio,webbrowser,wave
flag = 0
flag2 = 0
count = 0
count2 = 0
flag3=0
duration=0
n=0
app = Flask(__name__)


class RecAUD:

    def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=2, rate=44100, py=pyaudio.PyAudio()):

        # Start Tkinter and set Title
        self.collections = []
        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.p = py
        self.frames = []
        self.st = 1
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)




    def start_record(self):
        self.st = 1
        self.frames = []
        stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        while self.st == 1:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            global duration
            if duration>240:
                break
            duration+=1
            print(duration)
            #print("* recording")
        #if duration>20:
            #global status
            #status="TimeOut!"

        duration=0
        stream.close()
        filename = "output{}.wav".format(n)
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def stop(self):
        self.st = 0
#---------------------------------------------------------


cap = cv2.VideoCapture(0)


def gen_frames():
    while True:
        global count2, flag, count, flag2, flag3
        # Capture frame-by-frame
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        ret, img = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        face_count = len(faces)
        if face_count != 0:
            print("face_detected")
            count += 1

            count2 = 0
            flag = 1

            if flag == 2:
                count = 0
                flag = 1
            if count > 10 and flag2 == 3:
                print("***********playing sound . . . ")
                flag2 = 0
                count = 0
                webbrowser.open("http://127.0.0.1:5000/cool_form")

        else:

            count2 += 1
            count = 0
            if count2 > 10:
                flag2 = 3
                count2 = 0
            print("face_not_detected")
            # os.system("pkill chromium")
            if flag == 1:
                flag = 2
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
        # Process the frame
        # ...

        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        # Yield the frame in byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Sleep for a short time to control the frame rate
        time.sleep(0.1)


@app.route('/')
def index():
    return render_template('test3.html')
@app.route('/video_feed')
def video_feed():
    print("hello3")
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/cool_form', methods=['GET', 'POST'])
def cool_form():
    if request.method == 'POST':
        print("stop recording")
        guiAUD.stop()
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('test4.html')


@app.route("/start_recording", methods=["POST"])
def start_recording():
    print("recording_started")
    guiAUD.start_record()
    global n
    n += 1
    return "recording started"


if __name__ == '__main__':
    guiAUD = RecAUD()
    app.run(debug=True)
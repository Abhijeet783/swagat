
import socket, cv2, pickle, struct, imutils
from pydub import AudioSegment
from flask import Flask, Response,render_template, url_for, redirect,request
import pyaudio,webbrowser,wave
import time
from time import sleep
import RPi.GPIO as gpio
from pydub.playback import play
import threading
playing_finished=1

R_DIR= 8
R_STEP= 7
R_EN= 25

L_DIR= 23
L_STEP= 18
L_EN= 24

gpio.setmode(gpio.BCM)

gpio.setup(R_DIR, gpio.OUT)
gpio.setup(R_STEP, gpio.OUT)
gpio.setup(R_EN, gpio.OUT)
gpio.output(R_EN,0)

gpio.setup(L_DIR, gpio.OUT)
gpio.setup(L_STEP, gpio.OUT)
gpio.setup(L_EN, gpio.OUT)
gpio.output(L_EN,0)


flag = 0
flag2 = 0
count = 0
count2 = 0
flag3=0
duration=0
n=0

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '10.212.11.20'  # paste your server ip address here
port = 5001
client_socket.connect((host_ip, port))  # a tuple
data = b""
app = Flask(__name__)
vid = cv2.VideoCapture(0)


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

def hand_move():
    sleep(1)
    gpio.output(R_DIR, 0)
    gpio.output(L_DIR, 0)
    for x in range(450):
        gpio.output(R_STEP, gpio.HIGH)
        gpio.output(L_STEP, gpio.HIGH)
        sleep(0.001)
        gpio.output(R_STEP, gpio.LOW)
        gpio.output(L_STEP, gpio.LOW)
        sleep(0.001)
    sleep(1)
    gpio.output(R_DIR, 1)
    gpio.output(L_DIR, 1)
    for x in range(450):
        gpio.output(R_STEP, gpio.HIGH)
        gpio.output(L_STEP, gpio.HIGH)
        sleep(0.001)
        gpio.output(R_STEP, gpio.LOW)
        gpio.output(L_STEP, gpio.LOW)
        sleep(0.001)



def handle_client(client_socket):
    global playing_finished
    while True:
        message=client_socket.recv(1024).decode()
        if message and playing_finished:
            playing_finished=0
            print('received msg:',message)
            hand_move()
            song = AudioSegment.from_wav("1.wav")
            song2 = AudioSegment.from_wav("2.wav")
            print('playing...')
            play(song)
            play(song2)
            webbrowser.open("http://127.0.0.1:5000/cool_form")
            #playing_finished=1
def handle_client2(client_socket):
    while (vid.isOpened()):
        img, frame = vid.read()
        frame = imutils.resize(frame, width=320)
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        client_socket.sendall(message)




        #data = client_socket.recv(1024).decode()
        #print(data)

client_thread=threading.Thread(target=handle_client,args=(client_socket,))
client_thread2=threading.Thread(target=handle_client2,args=(client_socket,))
client_thread.start()
client_thread2.start()


def gen_frames():
    while True:
        success, frame = vid.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/')
def index():
    return render_template('test3_2.html')
@app.route('/video_feed')
def video_feed():
    print("hello3")
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/cool_form', methods=['GET', 'POST'])
def cool_form():
    global playing_finished
    if request.method == 'POST':
        print("stop recording")
        guiAUD.stop()
        song3 = AudioSegment.from_wav("3.wav")
        play(song3)
        playing_finished=1
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
    app.run(debug=False)


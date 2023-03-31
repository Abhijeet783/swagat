from flask import Flask, render_template, url_for, request
import webbrowser
import pyaudio
import wave
n=0
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 2

app = Flask(__name__)
def RecordingVoice1():
    print('recording')
 
def RecordingVoice():
    print('Recording...')
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=sample_format,\
                   channels=channels,\
                   rate=fs,\
                   frames_per_buffer=chunk,\
                   input=True)
    
    frames = []  # Initialize array to store frames
    
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    
    stream.stop_stream()
    
    stream.close()
    
    #p.terminate()
    
    print('Finished recording')
    
    filename = "/home/pi/welcome_voice_on_face_detect/audio_complaints/output{}.wav".format(n)
    #filename = "/home/pi/welcome_voice_on_face_detect/audio_complaints/output1.wav"
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    

@app.route('/')
@app.route('/home')
def home():
    return render_template("index2.html")



@app.route('/json')
def json():
    return render_template('index2.html')

#background process happening without any refreshing
@app.route('/background_process_test',methods=['POST', 'GET'])
def background_process_test():
    RecordingVoice()
    print("hello")
    status="Recording finished"
    global n
    n+=1
    return render_template('index2.html', status = status)


if __name__ == "__main__":

    app.run(debug=True)
    #RecordingVoice()




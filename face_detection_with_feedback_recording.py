import pyaudio
import wave
import cv2
from playsound import playsound
import sounddevice as sd
import wave


flag=0
flag2=0
count=0
count2=0
num=0
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 2


  # Create an interface to PortAudio

face_cascade = cv2.CascadeClassifier('/home/cdac/Downloads/FaceDetect-master/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)


while 1:

	ret, img = cap.read()


	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	face_count=len(faces)
	if face_count!=0:
		print("face_detected")
		count+=1
		count2=0
		flag=1

		if flag==2:
			count=0
			flag=1
		if count>10 and flag2==3:
			print("***********playing sound . . . ")
			
			playsound('/home/cdac/Desktop/Welcome to cdac.m4a')
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
			p.terminate()
			print('Finished recording')
			filename = "/home/cdac/Desktop/audio_feedback/output{}.wav".format(num)
			wf = wave.open(filename, 'wb')
			wf.setnchannels(channels)
			wf.setsampwidth(p.get_sample_size(sample_format))
			wf.setframerate(fs)
			wf.writeframes(b''.join(frames))
			wf.close()
			num+=1
			flag2=0
			count=0
	else:
		count2+=1
		count=0
		if count2>10:
			flag2=3
			count2=0
		print("face_not_detected")
		if flag==1:
			flag=2
	for (x,y,w,h) in faces:

		cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]


	cv2.imshow('img',img)


	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

cap.release()

cv2.destroyAllWindows()


import cv2
from pydub import AudioSegment
from pydub.playback import play
import webbrowser
import os
import time

flag=0
flag2=0
count=0
count2=0


def open_URL():
    webbrowser.open("http://127.0.0.1:5000/")

    #time.sleep(9)
    #os.system("pkill chromium")
    
    
        

face_cascade = cv2.CascadeClassifier('/home/pi/welcome_voice_on_face_detect/swagat/haarcascade_frontalface_default.xml')

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
			#playsound('/home/pi/Desktop/Welcome1.m4a')
			song = AudioSegment.from_wav("/home/pi/Downloads/Welcome1.wav")
			print('playing sound .....')
			play(song)
			open_URL()
			flag2=0
			count=0
	else:
		count2+=1
		count=0
		if count2>10:
			flag2=3
			count2=0
		print("face_not_detected")
		#os.system("pkill chromium")
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





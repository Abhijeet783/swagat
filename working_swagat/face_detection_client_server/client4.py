
import socket, cv2, pickle, struct, imutils
from pydub import AudioSegment
from flask import Flask, Response,render_template, url_for, redirect,request
import pyaudio,webbrowser,wave
import time
from time import sleep
#import RPi.GPIO as gpio
from pydub.playback import play
import threading
playing_finished=1

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '10.212.11.24'  # paste your server ip address here
port = 5001
client_socket.connect((host_ip, port))  # a tuple
data = b""

vid = cv2.VideoCapture(0)

def handle_client(client_socket):
    global playing_finished
    while True:
        message=client_socket.recv(1024).decode()
        if message and playing_finished:
            playing_finished=0
            print('received msg:',message)
            song = AudioSegment.from_wav("welcome.wav")
            print('playing...')
            play(song)
            playing_finished=1

while (vid.isOpened()):
    client_thread=threading.Thread(target=handle_client,args=(client_socket,))
    client_thread.start()
    img, frame = vid.read()
    frame = imutils.resize(frame, width=320)
    a = pickle.dumps(frame)
    message = struct.pack("Q", len(a)) + a
    client_socket.sendall(message)

    cv2.imshow('TRANSMITTING VIDEO', frame)
    key = cv2.waitKey(1) & 0xFF



    #data = client_socket.recv(1024).decode()
    #print(data)
    if key == ord('q'):
        client_socket.close()

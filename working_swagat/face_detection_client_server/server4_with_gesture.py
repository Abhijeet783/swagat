# This code can play video when gesture detected.

import socket, cv2, pickle, struct
import cv2, pickle
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
flag = 0
flag2 = 0
count = 0
count2 = 0
flag3=0
detected=0
permit_to_gesture=0
# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = '10.212.11.20'
print('HOST IP:', host_ip)
port = 5001
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(1)
print("LISTENING AT:", socket_address)
payload_size = struct.calcsize("Q")
data = b""
# Socket Accept
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
model = load_model('mp_hand_gesture')

# Load class names
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)

def handle_client(client_socket):
    while True:
        # Receive and process messages from the client
        data = 'detected'
        server_socket.send(data.encode())  # send data to the client
        # Process the received message as needed
        print("message sent:", message)

while True:
    #global count2, flag, count, flag2, flag3,detected
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        while True:
            while len(data) < payload_size:

                packet = client_socket.recv(4 * 1024)  # 4K
                if not packet: break
                data += packet

            packed_msg_size = data[:payload_size]

            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            frame_data = data[:msg_size]

            data = data[msg_size:]

            img = pickle.loads(frame_data)

#.........................................
            if permit_to_gesture==0 :
                face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
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
                        #client_thread = threading.Thread(target=handle_client, args=(client_socket,))
                        #client_thread.start()
                        #client_thread.join()
                        response = "face_detected"
                        client_socket.send(response.encode('utf-8'))
                        permit_to_gesture=1
                        flag2 = 0
                        count = 0

                else:

                    count2 += 1
                    count = 0
                    if count2 > 10:
                        flag2 = 3
                        count2 = 0
                    print("face_not_detected")

                    if flag == 1:
                        flag = 2
#-------------------------------------------------------------------
            else :
                x, y, c = img.shape

                # Flip the frame vertically
                img = cv2.flip(img, 1)
                framergb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # Get hand landmark prediction
                result = hands.process(framergb)

                # print(result)

                className = ''

                # post process the result
                if result.multi_hand_landmarks:
                    landmarks = []
                    for handslms in result.multi_hand_landmarks:
                        for lm in handslms.landmark:
                            # print(id, lm)
                            lmx = int(lm.x * x)
                            lmy = int(lm.y * y)

                            landmarks.append([lmx, lmy])

                        # Drawing landmarks on frames
                        mpDraw.draw_landmarks(img, handslms, mpHands.HAND_CONNECTIONS)

                        # Predict gesture
                        prediction = model.predict([landmarks])
                        # print(prediction)
                        classID = np.argmax(prediction)
                        className = classNames[classID]
                        if className == 'rock':
                            print('playing video1!')
                            response = "rock"
                            client_socket.send(response.encode('utf-8'))
                        elif className == 'thumbs up':
                            print('playing video2!')
                            response = "thumbs_up"
                            client_socket.send(response.encode('utf-8'))
                        elif className == 'thumbs down':
                            print('playing video3!')
                            response = "thumbs_down"
                            client_socket.send(response.encode('utf-8'))
                        elif className == 'fist':
                            print('playing video4!')
                            response = "fist"
                            client_socket.send(response.encode('utf-8'))
                        elif className == 'okay':
                            print('stop!')
                            response = "stop"
                            permit_to_gesture=0
                            client_socket.send(response.encode('utf-8'))

                # show the prediction on the frame
                cv2.putText(img, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2, cv2.LINE_AA)

                # Show the final output
                cv2.imshow("Output", img)

            #............................................
            #cv2.imshow("RECEIVING VIDEO", img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()